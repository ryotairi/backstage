import logging
import sys

# Configure the logger
_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s"))

logger = logging.getLogger("libresekai")
logger.setLevel(logging.DEBUG)
logger.addHandler(_handler)
