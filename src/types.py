from pathlib import Path
from enum import StrEnum, Enum


class Datasets(StrEnum):
    gse_68849 = "GSE68849"


class DataPaths(Enum):
    base_dir: Path = Path("data")
    output_dir: Path = Path("data/output")
    tsv: Path = Path("data/tsv")
