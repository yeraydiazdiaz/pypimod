from logging import getLogger
from logging.config import dictConfig
from pypimod.config import settings

dictConfig(settings.LOGGING)

get_logger = getLogger
