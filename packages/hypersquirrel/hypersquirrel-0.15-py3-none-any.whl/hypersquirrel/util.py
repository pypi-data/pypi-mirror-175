import requests
from commmons import html_from_url
from bs4 import BeautifulSoup


def html_from_url_with_headers(url, referer=None):
    return html_from_url(url, headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Referer": referer or url
    })


def html_from_url_with_bs4(url, referer=None):
    r = requests.get(url, headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Referer": referer or url
    })
    return BeautifulSoup(r.text, "lxml")
