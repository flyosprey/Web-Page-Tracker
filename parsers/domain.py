import re
import time
from urllib.parse import urlparse
from typing import Dict, Set, Optional
import concurrent.futures
import threading
from queue import Queue
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup, SoupStrainer


from parsers.basic.main_spider import Spider
from parsers.basic.headers_preparator import HeadersPreparatorInterface
from loggers.domain_logger import domain_logger


class DomainSpider(Spider):
    __lock = threading.Lock()

    def __init__(self, domain: str, headers_behavior: Optional[HeadersPreparatorInterface] = None):
        self.__domain = domain
        self.__basic_url = f"https://{self.__domain}"
        self.__threads_queue = Queue()
        super().__init__(headers_behavior)

    def get_result(self) -> Dict:
        return self.__calculate_result()

    def __calculate_result(self) -> Dict:
        with requests.Session() as session:
            if self._headers is not None:
                session.headers.update(self._headers)
            result = {"active_page_count": 0, "total_page_count": 0, "url_list": set()}
            self.__search_by_url({self.__basic_url}, result, session)
            result["url_list"] = list(result["url_list"])
        return result

    def __search_by_url(self, urls: Set[str], result: Dict, session: requests.Session) -> Dict:
        if not urls:
            return result
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self.__get_url_info, url, session) for url in urls]
            for future in concurrent.futures.as_completed(futures):
                url_info = future.result()
                result["url_list"] = result["url_list"] | url_info["url_list"]
                result["active_page_count"] += url_info["active_page_count"]
                result["total_page_count"] += url_info["total_page_count"]
                domain_urls = url_info.get("domain_urls")
                if domain_urls:
                    result = self.__search_by_url(domain_urls, result, session)

        return result

    def __get_url_info(self, url: str, session: requests.Session) -> Dict:
        sub_result = {"active_page_count": 0, "total_page_count": 0, "url_list": set()}
        if url == self.__basic_url + "/" or url in self.__threads_queue.queue:
            return sub_result

        with self.__lock:
            self.__threads_queue.put(url)
        try:
            response = self.__send_request(url, session)
            if response.status_code == 200:
                domain_urls = self.__get_domain_urls(response)
                sub_result["active_page_count"] += 1
                sub_result["domain_urls"] = domain_urls
        except RequestException:
            domain_logger.info(f"%s -> RequestException" % url)
        finally:
            sub_result["total_page_count"] += 1
            sub_result["url_list"].add(url)

        return sub_result

    def __send_request(self, url: str, session: requests.Session) -> requests.Response:
        response = session.get(url, allow_redirects=True, timeout=2)
        domain_logger.info(f"%s -> %s" % (url, response.status_code))
        if response.status_code in (429,):
            self.__retry(url, response, session)

        return response

    def __retry(self, url: str, response: requests.Response, session: requests.Session) -> requests.Response:
        max_retries, retries, wait_time = 3, 0, 2
        while response.status_code != 200 and max_retries > retries:
            time.sleep(wait_time)
            response = self.__send_request(url, session)
            retries += 1
        if retries == max_retries and response.status_code != 200:
            raise RequestException

        return response

    def __get_domain_urls(self, response: requests.Response) -> Set:
        soup = BeautifulSoup(response.text, 'html.parser', parse_only=SoupStrainer("a"))
        domain_a_tags = soup.find_all('a', href=self.__links_filter)
        domain_urls = set()
        for tag in domain_a_tags:
            href = tag.attrs["href"]
            href = re.sub(r"#.*|\?.*", "", href)
            if self.__domain in href:
                domain_urls.add(href)
            else:
                domain_urls.add(self.__basic_url + href)

        return domain_urls

    def __links_filter(self, href) -> bool:
        return urlparse(href).netloc == self.__domain or bool(re.search(r"^/\S+", str(href)))
