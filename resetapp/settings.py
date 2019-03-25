import logging
from os import getenv

CACHE_EXPIRES = 20
CACHE_CONTROL = f'max-age={CACHE_EXPIRES}'


LOG_FMT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LVL = logging.INFO

ENVIRON = getenv("ENV", "DEV")

PAGE_SIZE = 50
