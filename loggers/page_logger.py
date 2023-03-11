import logging


page_logger = logging.getLogger(__name__)
page_logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/pages.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
page_logger.addHandler(handler)
