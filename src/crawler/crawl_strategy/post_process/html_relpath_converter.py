#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

# Created by wab2pal at 5/10/23

from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

class HtmlRelpathConverter:

    @staticmethod
    def handle(soup: BeautifulSoup, base_url: str):
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link['href']
            if base_url and not bool(urlparse(href).netloc):
                updated_href = urljoin(base_url, href)
                link['href'] = updated_href

        all_imgs = soup.find_all('img', src=True)
        for img in all_imgs:
            src = img['src']
            if base_url and not bool(urlparse(src).netloc):
                updated_src = urljoin(base_url, src)
                img['src'] = updated_src

        return
