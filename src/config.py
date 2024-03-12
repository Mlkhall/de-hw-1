from pydantic_settings import BaseSettings
from yarl import URL


class DataSourceSettings(BaseSettings):
    ncbi_dsn: URL = URL("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi")
