import gzip
import io
import os
import re
import tarfile
from collections import defaultdict
from datetime import datetime, timezone
from typing import Literal

import luigi
import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger
from yarl import URL

from src.config import DataSourceSettings
from src.types import DataPaths, Datasets


class NCBIEndpointDatasetGetterTask(luigi.Task):

    data_sources = DataSourceSettings()
    dataset_name: Datasets = luigi.Parameter(default=Datasets.gse_68849)

    def run(self):
        logger.info("Running EndpointDatasetGetterTask...")
        ncbi_page = self._get_ncbi_download_page()
        download_endpoint = self._parse_download_endpoint(ncbi_page)
        logger.success("Got NCBI page!")

        with open(self.output().path, "w") as f:
            f.write(str(download_endpoint))
            logger.success(
                f"Saved download endpoint {download_endpoint} to {self.output().path}"
            )

    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget(
            f"{DataPaths.output.value}/{self.dataset_name}_url.txt"
        )

    def complete(self):
        return self.output().exists()

    def _parse_download_endpoint(self, page: BeautifulSoup) -> URL:
        all_a_tags = page.find_all("a")
        ncbi_set_download_url = None
        for a_tag in all_a_tags:
            if a_tag.text == "(http)":
                ncbi_set_download_url = a_tag["href"]
                break

        if ncbi_set_download_url is None:
            raise ValueError("No download link found!")

        return URL(
            f"{self.data_sources.ncbi_dsn.scheme}://"
            f"{self.data_sources.ncbi_dsn.host}"
            f"{ncbi_set_download_url}"
        )

    def _get_ncbi_download_page(self) -> BeautifulSoup:
        page_url = self._ncbi_download_page_url
        response = requests.get(page_url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    @property
    def _ncbi_download_page_url(self) -> URL:
        return self.data_sources.ncbi_dsn % {"acc": self.dataset_name}


class NCBIArchiveLoaderTask(luigi.Task):

    def requires(self):
        return NCBIEndpointDatasetGetterTask()

    def run(self):
        logger.info("Running NCBIArchiveLoader...")

        with self.input().open("r") as f:
            download_endpoint = URL(f.read())

        logger.info(f"Downloading archive from {download_endpoint}...")
        response = requests.get(url=download_endpoint, allow_redirects=True)
        response.raise_for_status()
        logger.success(f"Downloaded archive from {download_endpoint}!")

        with open(self.output().path, "wb") as file:
            file.write(response.content)
            logger.success(f"Saved archive to {self.output().path}")

    def output(self):
        dataset_name = "NCBI_GEO_Dataset"
        archive_name = f"{dataset_name}_RAW.tar"
        archive_file_path = f"{DataPaths.output.value}/{archive_name}"
        return luigi.LocalTarget(archive_file_path)

    @classmethod
    def _parse_archive_file_name(cls, http_headers: dict) -> str:
        match = re.search(
            r'filename="([^"]+\.tar)', http_headers["Content-Disposition"]
        )
        if not match:
            raise FileNotFoundError("No filename found in Content-Disposition header!")

        return match.group(1)


class NCBIExtractTarFileTask(luigi.Task):

    def requires(self):
        return NCBIArchiveLoaderTask()

    def run(self):
        with tarfile.open(self.input().path, "r") as tar:
            tar.extractall(path=DataPaths.output.value)
            logger.success(
                f"Extracted archive {self.input().path} to {DataPaths.output.value}!"
            )

        datasets_gz_files = self._get_txt_gx_files_names(
            directory_path=DataPaths.output.value
        )
        unzip_files_paths = self._unzip_gz_files(gz_files=datasets_gz_files)
        self._drop_gz_files(gz_files=datasets_gz_files)

        with open(self.output().path, "w") as f:
            f.write("\n".join(unzip_files_paths))
            logger.success(f"Saved extracted files to {self.output().path}")

    def output(self):
        return luigi.LocalTarget(f"{DataPaths.output.value}/extracted_files.txt")

    @classmethod
    def _get_txt_gx_files_names(cls, directory_path: str) -> tuple[str, ...]:
        return tuple(
            file_name
            for file_name in os.listdir(directory_path)
            if file_name.endswith(".txt.gz")
        )

    @classmethod
    def _unzip_gz_files(cls, gz_files: tuple[str, ...]) -> list[str]:
        unzip_files = []
        for gz_file in gz_files:
            file_path = f"{DataPaths.output.value}/{gz_file}"

            with gzip.open(file_path, "rb") as file_input:
                unzip_file = gz_file.replace(".gz", "")
                unzip_file_path = f"{DataPaths.base.value}/{unzip_file}"
                with open(unzip_file_path, "wb") as file_output:
                    file_output.write(file_input.read())

                unzip_files.append(unzip_file_path)

        return unzip_files

    @classmethod
    def _drop_gz_files(cls, gz_files: tuple[str, ...]):
        for gz_file in gz_files:
            os.remove(f"{DataPaths.output.value}/{gz_file}")


class NCBIDataSetsProcessingTask(luigi.Task):

    def requires(self):
        return NCBIExtractTarFileTask()

    def run(self):

        raw_datasets = self._get_raw_datasets()
        datasets = defaultdict(list)
        for raw_dataset in raw_datasets:
            raw_dataset_file_path = f"{DataPaths.base.value}/{raw_dataset}"
            dfs = self._process_raw_datasets(raw_dataset_file_path)

            for key, df in dfs.items():
                datasets[key].append(df)

        processed_datasets = {}
        for key, dfs in datasets.items():
            df = pd.concat(dfs)
            processed_datasets[key] = df

        self._save_processed_datasets(processed_datasets=processed_datasets)
        self._special_processing(processed_datasets=processed_datasets)
        self._drop_unnecessary_files()

    def output(self):
        return tuple(
            luigi.LocalTarget(f"{DataPaths.tsv.value}/{file_name}")
            for file_name in os.listdir(DataPaths.tsv.value)
            if file_name.endswith(".tsv")
        )

    @classmethod
    def _get_raw_datasets(cls):
        return tuple(
            file_name
            for file_name in os.listdir(DataPaths.base.value)
            if file_name.endswith(".txt")
        )

    @classmethod
    def _process_raw_datasets(
        cls, raw_dataset_file_path: str
    ) -> dict[str, pd.DataFrame]:
        dfs = {}
        write_key = None

        with open(raw_dataset_file_path) as file:
            fio = io.StringIO()

            for raw_line in file.readlines():
                if raw_line.startswith("["):
                    if write_key:
                        fio.seek(0)
                        header = None if write_key == "Heading" else "infer"
                        dfs[write_key] = pd.read_csv(fio, sep="\t", header=header)
                    fio = io.StringIO()
                    write_key = raw_line.strip("[]\n")
                    continue

                if write_key:
                    fio.write(raw_line)
            fio.seek(0)

            dfs[write_key] = pd.read_csv(fio, sep="\t")
        return dfs

    @classmethod
    def _save_processed_datasets(
        cls,
        processed_datasets: dict[str, pd.DataFrame],
        type_: Literal["FULL", "PARTIAL"] = "FULL",
    ) -> None:
        for key, df in processed_datasets.items():
            file_name = f"{key}_{type_}_{datetime.now(tz=timezone.utc)}.tsv"
            file_name = file_name.replace(" ", "_")
            file_path = f"{DataPaths.tsv.value}/{file_name}"
            df.to_csv(file_path, sep="\t", index=False)
            logger.success(f"Saved processed dataset to {file_path}")

    @classmethod
    def _special_processing(cls, processed_datasets: dict[str, pd.DataFrame]) -> None:
        special_key = "Probes"
        special_df = processed_datasets[special_key]

        special_df.drop(
            columns=[
                "Definition",
                "Ontology_Component",
                "Ontology_Process",
                "Obsolete_Probe_Id",
                "Probe_Sequence",
                "Synonyms",
                "Ontology_Function",
            ],
            inplace=True,
        )

        cls._save_processed_datasets(
            processed_datasets={special_key: special_df}, type_="PARTIAL"
        )

    @classmethod
    def _drop_unnecessary_files(cls) -> None:
        for file_name in os.listdir(DataPaths.base.value):
            file_path = f"{DataPaths.base.value}/{file_name}"
            if file_name.endswith(".txt"):
                os.remove(file_path)
                logger.success(f"Removed {file_path}")
