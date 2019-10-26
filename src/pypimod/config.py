from pathlib import Path
import os

import environ
import envfiles

HERE = Path(__file__).absolute()
DEV_PATH = HERE.parents[2] / "dev"


@environ.config(prefix="PPM")
class Config:
    GC_CREDENTIALS: str = environ.var()
    GC_PROJECT: str = environ.var()

    BQ_PYPI_DOWNLOADS_TABLE: str = environ.var("the-psf.pypi.downloads*")
    CACHE_RESULTS: bool = environ.bool_var(True)
    CACHED_RESULTS_PATH: str = environ.var(DEV_PATH / "cached_bq_results.json")

    SERVER_HOST: str = environ.var("0.0.0.0", name="HOST")
    SERVER_PORT: int = environ.var(8080, converter=int, name="PORT")

    GITHUB_SECRET: str = environ.var()
    GITHUB_AUTH: str = environ.var()
    GITHUB_REPO: str = environ.var("yeraydiazdiaz/pypimod")


env_file = os.getenv("ENV_FILE")
if env_file:
    env = envfiles.load(env_file)
    env.update(os.environ)
else:
    env = os.environ

settings = environ.to_config(Config, env)
