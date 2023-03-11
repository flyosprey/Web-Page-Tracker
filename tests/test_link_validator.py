import pytest
from custom_validators.link_validator import LinkValidator, UrlValidatorError, DomainValidatorError
from urllib.parse import quote

VALID_URLS = ("https://southdakotamastergardener.com/about/", "https://www.sirinakornpaint.com/",
              "http://flogger1207.blogspot.com/feeds/posts/default", "https://www9.myasiantv.io/contact",
              "http://salariodigno.mx/new/watch-divorcio-mortal-en-espaol.html",
              "http://salariodigno.mx/online/pelcula-south32-en-lnea.html", "https://tainico.tumblr.com/#_=_",
              "http://imkbilkokulu.meb.k12.tr/icerikler/hizmet-standartlari_8194964.html",
              "http://old-ru.ru/vrata.html",
              "http://izmirtemizliksirketifiyatlari.blogspot.com/search/label/ev temizliği şirketleri",
              "http://360buildingsolutions.co.uk/privacy-policy-2/", "http://hotel-gasthof-ritter.de/?page_id=286",
              "https://www.7-eleven.com.ph/customer-care/", "http://bfrr.net/члены-бфрр/членские-взносы-2015/",
              "http://bfrr.net/члены-бфрр/членские-взносы-2015/",)

INVALID_URLS = ("htp:/southdakotamastergardener.com/about/", "https:www.sirinakornpaint.com/",
                "http//flogger1207.blogspot.com/feeds/posts/default", "httpss://www9.myasiantv.io/contact",
                "htt://salariodigno.mx/new/watch-divorcio-mortal-en-espaol.html", "http:///old-ru.ru/vrata.html",)

VALID_DOMAINS = {"https://southdakotamastergardener.com/about/": "southdakotamastergardener.com",
                 "http://old-ru.ru/vrata.html": "old-ru.ru",
                 "http://360buildingsolutions.co.uk/privacy-policy-2/": "360buildingsolutions.co.uk",
                 "https://www.7-eleven.com.ph/customer-care/": "www.7-eleven.com.ph",
                 "http://flogger1207.blogspot.com/feeds/posts/default": "flogger1207.blogspot.com",
                 "http://bfrr.net/члены-бфрр/членские-взносы-2015/": "bfrr.net"}

ERROR_DOMAIN = ("htp:/southdakotamastergardener/about/", "https:com/", "net", "old-ru")


def test_valid_url():
    for url in VALID_URLS:
        normalized_url = quote(url, safe=":/")
        url = LinkValidator.normalize_url(url)

        assert url == normalized_url


def test_invalid_url():
    for url in INVALID_URLS:
        with pytest.raises(UrlValidatorError, match=r"^Bad URL.*"):
            LinkValidator.normalize_url(url)


def test_valid_domain():
    for url in VALID_DOMAINS.keys():
        domain = VALID_DOMAINS[url]
        checked_domain = LinkValidator.normalize_domain(domain)
        normalized_domain = LinkValidator.normalize_domain(url)

        assert normalized_domain == domain
        assert checked_domain == domain


def test_invalid_domain():
    for domain in ERROR_DOMAIN:
        with pytest.raises(DomainValidatorError, match=r"^Bad domain.*"):
            LinkValidator.normalize_domain(domain)
