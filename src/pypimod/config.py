from pathlib import Path
import os

import environ
import envfiles

HERE = Path(__file__).absolute()
DEV_PATH = HERE.parents[2] / "dev"


@environ.config(prefix="PPM")
class Config:
    GC_CREDENTIALS = environ.var()
    GC_PROJECT = environ.var()

    BQ_PYPI_DOWNLOADS_TABLE = environ.var("the-psf.pypi.downloads*")
    CACHE_RESULTS = environ.bool_var(True)
    CACHED_RESULTS_PATH = environ.var(DEV_PATH / "cached_bq_results.json")


env_file = os.getenv("ENV_FILE")
if env_file:
    env = envfiles.load(env_file)
    env.update(os.environ)
else:
    env = os.environ

settings = environ.to_config(Config, env)
