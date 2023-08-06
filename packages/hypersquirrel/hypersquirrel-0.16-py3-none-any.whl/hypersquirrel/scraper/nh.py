from typing import Optional

from bs4 import Tag, BeautifulSoup
from commmons import get_host_url, breakdown

from hypersquirrel.util import html_from_url_with_bs4 as html_from_url


def get_vkey_href_title(li: Tag):
    vkey: str = li.attrs.get("data-video-vkey")
    href = f"view_video.php?viewkey={vkey}"
    title = None
    a = li.find("a", attrs=dict(href=f"/{href}"))
    if a:
        title = a.attrs.get("title")
    return vkey, href, title


def get_profile_name(soup: BeautifulSoup) -> Optional[str]:
    div = soup.find("div", class_="nameSubscribe")
    if div:
        return div.find("h1").text.strip()


def scrape(url):
    url, params = breakdown(url)
    soup = html_from_url(url, params=params)
    profile_name = get_profile_name(soup)

    for li in soup.find_all("li", class_="videoblock"):
        def try_append_uploader(title: str) -> str:
            uploader = profile_name
            if not uploader:
                usrdiv = li.find("div", class_="usernameWrap")
                if usrdiv:
                    uploader = usrdiv.find("a").text

            return f"[{uploader}] {title}" if uploader else title

        vkey, href, title = get_vkey_href_title(li)
        if title:
            file = dict(
                fileid=vkey,
                sourceurl=f"{get_host_url(url)}/{href}",
                filename=try_append_uploader(title.strip())
            )

            thumbnailurl = li.find("img", class_="thumb", attrs=dict(title=title)).attrs.get("data-src")
            if thumbnailurl:
                file["thumbnailurl"] = thumbnailurl

            yield file


if __name__ == '__main__':
    import json

    files = list(scrape("https://www.pornhub.com/view_video.php?viewkey=ph61575828c929b"))
    print(json.dumps(files, indent=2))
