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

    SERVER_HOST: str = environ.var("0.0.0.0")
    SERVER_PORT: int = environ.var(8080, converter=int)

    GITHUB_SECRET: str = environ.var()
    GITHUB_KEY: str = environ.var()
    GITHUB_OWNER: str = environ.var("yeraydiazdiaz")
    GITHUB_REPO: str = environ.var("pypimod")
    GITHUB_APP_ID: int = environ.var(44773, converter=int)

    @property
    def GITHUB_REPO_PATH(self):
        return "/".join((self.GITHUB_OWNER, self.GITHUB_REPO))

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
