import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

