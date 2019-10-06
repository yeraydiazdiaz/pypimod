from pathlib import Path
import typing
import os

import environ

HERE = Path(__file__).absolute()
DEV_PATH = HERE.parents[2] / "dev"
ENV_PATH = DEV_PATH / "local.env"


@environ.config(prefix="PPM")
class Config:
    GC_CREDENTIALS = environ.var()
    GC_PROJECT = environ.var()

    BQ_PYPI_DOWNLOADS_TABLE = environ.var("the-psf.pypi.downloads*")
    CACHED_RESULTS_PATH = environ.var(DEV_PATH / "cached_bq_results.json")


def read_env_file(env_file_path: typing.Union[Path, str]) -> dict:
    env = {}
    with open(env_file_path) as fd:
        for line in fd.readlines():
            line = line.strip()
            if line.startswith("#"):
                continue
            k, v = line.split("=", maxsplit=1)
            # TODO: remove quotes on value
            env[k] = v

    return env


env = None
if ENV_PATH.exists():
    env = read_env_file(ENV_PATH)
    env.update(os.environ)

settings = environ.to_config(Config, env)
