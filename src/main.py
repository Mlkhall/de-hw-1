import luigi

from src.pipelines import (
    NCBIArchiveLoaderTask,
    NCBIDataSetsProcessingTask,
    NCBIEndpointDatasetGetterTask,
    NCBIExtractTarFileTask,
)

if __name__ == "__main__":
    luigi.build(
        [
            NCBIArchiveLoaderTask(),
            NCBIEndpointDatasetGetterTask(),
            NCBIExtractTarFileTask(),
            NCBIDataSetsProcessingTask(),
        ],
        workers=1,
        local_scheduler=True,
        no_lock=False,
    )
