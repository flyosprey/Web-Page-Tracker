import re
from urllib.parse import quote
import validators


class UrlValidatorError(Exception):
    pass


class DomainValidatorError(Exception):
    pass


class LinkValidator:
    @staticmethod
    def normalize_url(url: str) -> str:
        normalized_url = quote(url, safe=":/")
        is_valid = validators.url(normalized_url)
        if is_valid:
            return normalized_url
        raise UrlValidatorError("Bad url address! Check schema and domain")

    @staticmethod
    def normalize_domain(domain: str) -> str:
        basic_domain_regex = "((www\w*?\.)?[\w.-]+?)"
        domain = re.search(rf"{basic_domain_regex}/|{basic_domain_regex}$", domain)
        if domain:
            domain = domain[1] or domain[3]
            if validators.domain(domain):
                return domain
        raise DomainValidatorError("Bad domain!")
