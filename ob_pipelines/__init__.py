import logging
import os

from mongoengine import connect

from ob_pipelines.config import settings

logger = logging.getLogger(__name__)

# Create the format
formatter = logging.Formatter('%(asctime)s - %(message)s')

# Add a console handler
ch = logging.StreamHandler()
ch.setLevel(os.environ.get('LOGGING_LEVEL') or logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

connect(host=settings.db_connection)
