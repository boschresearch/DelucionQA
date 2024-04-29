#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

# Created by wab2pal at 5/16/23
import base64
import os
from typing import List
from urllib.parse import urlparse

import config.root_path as rp
from crawler.crawl_strategy.crawl_playright import CrawlPlayright

from playwright.sync_api import sync_playwright, Page, expect, Browser, BrowserContext, PlaywrightContextManager
from playwright.sync_api import TimeoutError


class ImgCrawler:

    def __init__(self):
        pass

    def crawl_img_list(self, img_url_list: List[str], path_list: List[str]):
        with sync_playwright() as p:
            try:
                browser, page, context = CrawlPlayright.init_browser_page_allow_BoschAuth(p)

                for img_url, path_str in zip(img_url_list, path_list):
                    if isinstance(page, Page):
                        page.goto(img_url)
                        path = rp.getRootPath() / path_str
                        #page.screenshot(omit_background=True, path=path)

                        image_element = page.locator('img').nth(0)
                        image_b64 = image_element.evaluate("""element => {
                              var cnv = document.createElement('canvas');
                              cnv.width = element.naturalWidth;
                              cnv.height = element.naturalHeight;
                              cnv.getContext('2d').drawImage(element, 0, 0, element.naturalWidth, element.naturalHeight);
                              return cnv.toDataURL().substring(22)
                            }""")
                        with open(path, 'wb') as f:
                            f.write(base64.b64decode(image_b64))

                page.close()

            except Exception as e:
                print(e)
            finally:
                pass

        return

if __name__ == '__main__':
    crawler = ImgCrawler()
    url = "https://inside-docupedia.bosch.com/confluence/download/thumbnails/841846123/SMI567_prods.png?version=1&modificationDate=1557501563000&api=v2"
    path = './data/crawl/temp/temp_2.png'
    crawler.crawl_img_list([url], [path])
