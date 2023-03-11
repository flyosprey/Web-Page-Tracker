import logging


domain_logger = logging.getLogger(__name__)
domain_logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/stats.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
domain_logger.addHandler(handler)
