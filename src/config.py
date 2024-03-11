from yarl import URL
from pydantic_settings import BaseSettings


class DataSourceSettings(BaseSettings):
    ncbi_dsn: URL = URL("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi")
