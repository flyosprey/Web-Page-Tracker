from typing import Dict
from abc import ABC, abstractmethod
import logging

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


class HeadersPreparatorInterface(ABC):
    @abstractmethod
    def _prepare_headers(self):
        pass

    @abstractmethod
    def _prepare_user_agent(self):
        pass

    @abstractmethod
    def get_headers(self):
        pass


class HeadersWithSchemas(HeadersPreparatorInterface):
    def _prepare_headers(self) -> Dict:
        user_agent = self._prepare_user_agent()
        logging.debug(user_agent)
        headers = {
            'accept': '*/*',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'user-agent': user_agent
        }
        return headers

    def _prepare_user_agent(self) -> str:
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=20)
        user_agent = user_agent_rotator.get_random_user_agent()
        return user_agent

    def get_headers(self) -> Dict:
        headers = self._prepare_headers()
        return headers
