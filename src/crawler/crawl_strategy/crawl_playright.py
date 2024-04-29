#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

# Created by wab2pal at 5/2/23
from __future__ import annotations

from playwright.sync_api import sync_playwright, Page, expect, Browser, BrowserContext, PlaywrightContextManager
from playwright.sync_api import TimeoutError

import config.root_path as rp
class CrawlPlayright:

    default_timeout = 200000

    @staticmethod
    def crawl_sync(url) -> str:
        html_content = None
        with sync_playwright() as p:
            browser, page, context = CrawlPlayright.init_browser_page_allow_BoschAuth(p)
            if isinstance(page, Page):
                page.goto(url)
                html_content = page.content()

            p.close()

        return html_content

    @staticmethod
    def init_browser_page_allow_BoschAuth(p: PlaywrightContextManager, downloads_path:str=None) -> (Browser, Page, object):

        browser = None

        if downloads_path:
            browser = p.chromium.launch(
                headless=True,
                downloads_path=downloads_path,
                args=[
                    "--auth-server-allowlist=*.bosch.com"
                ])
        else:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--auth-server-allowlist=*.bosch.com"
                ])

        context = browser.new_context()
        page = context.new_page()

        try:
            timeout = CrawlPlayright.default_timeout
            page.set_default_timeout(timeout)

        except Exception as e:
            print(e)
        finally:
            pass

        return browser, page, context




