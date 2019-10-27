from logging import getLogger
from logging.config import dictConfig

from quart.logging import default_handler
from pypimod.config import settings

getLogger("quart.app").removeHandler(default_handler)
getLogger("quart.serving").removeHandler(default_handler)
dictConfig(settings.LOGGING)
