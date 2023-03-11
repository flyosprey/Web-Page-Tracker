from typing import Dict, Optional
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup, SoupStrainer


from requests.exceptions import RequestException
from parsers.basic.main_spider import Spider
from parsers.basic.headers_preparator import HeadersPreparatorInterface


class PageSpider(Spider):
    def __init__(self, url: str, headers_behavior: Optional[HeadersPreparatorInterface] = None):
        self.__url = url
        super().__init__(headers_behavior)

    def get_result(self) -> Dict:
        return self.__calculate_result()

    def __calculate_result(self) -> Dict:
        session = requests.Session()
        if self._headers is not None:
            session.headers.update(self._headers)
        try:
            response = session.get(self.__url, allow_redirects=True, timeout=3)

            return self.__parse_response(response)
        except RequestException:
            raise RequestException

    def __parse_response(self, response: requests.Response) -> Dict:
        result = self.__fill_status_info(response)
        result["title"] = self.__get_title(response)
        result["domain_name"] = urlparse(response.url).hostname
        return result

    @staticmethod
    def __get_title(response: requests.Response) -> str:
        title = BeautifulSoup(response.content, "html.parser", parse_only=SoupStrainer("title")).text
        if title:
            return title.strip()
        raise Exception("ERROR: Failed to extract 'title'")

    def __fill_status_info(self, response: requests.Response) -> Dict:
        status_code, final_status_code, final_url = response.status_code, None, response.url
        if response.history:
            final_status_code = response.status_code
            status_code = response.history[0].status_code

        return {
            "status_code": status_code,
            "final_status_code": final_status_code,
            "final_url": final_url,
            "url": self.__url
        }
