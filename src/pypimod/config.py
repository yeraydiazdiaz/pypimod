from pathlib import Path
import os

import environ
import envfiles

HERE = Path(__file__).absolute()
CACHE_PATH = HERE.parents[2] / ".cache"


@environ.config(prefix="PPM")
class Config:

    GC_CREDENTIALS: str = environ.var()  # Path to Google JSON credentials
    GC_PROJECT: str = environ.var()
    BQ_PYPI_DOWNLOADS_TABLE: str = environ.var("the-psf.pypi.downloads*")
    CACHE_RESULTS: bool = environ.bool_var(True)
    CACHED_RESULTS_PATH: str = environ.var(CACHE_PATH / "cached_bq_results.json")

    LOGGING_LEVEL: str = environ.var("INFO")

    @property
    def LOGGING(self):
        return {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": self.LOGGING_LEVEL,
                    "formatter": "default",
                }
            },
            "loggers": {
                "": {
                    "handlers": ["console"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": True,
                }
            },
        }


env_file = os.getenv("ENV_FILE")
if env_file:
    env = envfiles.load(env_file)
    env.update(os.environ)
else:
    env = os.environ

settings = environ.to_config(Config, env)
