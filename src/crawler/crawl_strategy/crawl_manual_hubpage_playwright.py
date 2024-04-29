#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

## @author: Bingqing
from __future__ import annotations

import re
import logging
from pathlib import Path
from typing import List, Dict
from copy import copy

from playwright.sync_api import sync_playwright, Page, expect, Browser, BrowserContext
from playwright.sync_api import TimeoutError


from crawler.crawl_strategy.abs_crawl_manual_hugpage import AbsCrawlManualHubpage

from crawler.data_structure.manual_page_meta import ManualPageMeta, UtilityManualPageMeta
from crawler.data_structure.manual_page_store_item import ManualPageStoreItem
import config.root_path as rp

logger = logging.getLogger(__name__)

class CrawlManualHubpagePlaywright(AbsCrawlManualHubpage):

    default_timeout = 200000

    def crawl_all_subtopics(self, manual_page_meta: ManualPageMeta, page_collection: List[ManualPageStoreItem], crawl_param:Dict = {'headless': True} ):

        headless = crawl_param['headless'] if crawl_param and 'headless' in crawl_param else False

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            #browser = p.chromium.launch(
            #    headless=False,
                #downloads_path=downloads_path,
            #    args=[
            #        "--auth-server-allowlist=*.bosch.com"
            #    ])
            context = browser.new_context()
            page = context.new_page()

            UtilityManualPageMeta.clean_chapter_section_title(manual_page_meta)
            url_hubpage = UtilityManualPageMeta.get_manual_hubpage_url(manual_page_meta)

            path_html, path_html_individual = UtilityManualPageMeta.get_store_path(manual_page_meta)

            try:
                timeout = CrawlManualHubpagePlaywright.default_timeout
                page.set_default_timeout(timeout)
                page.goto(url_hubpage)

                manual_page_meta_curr: ManualPageMeta =  copy(manual_page_meta)
                html_curr = page.content()

                manual_page_store_item = ManualPageStoreItem(**manual_page_meta_curr.model_dump(),
                                                             path_html=path_html,
                                                             html=html_curr,
                                                             path_html_individual=path_html_individual,
                                                             html_individual=html_curr)
                page_collection.append(manual_page_store_item)

                # page.on("dialog", lambda dialog: dialog.accept())
                # page.get_by_role("button").click()

                print('page loaded, start parsing the page')

                page.locator('//*[@id="onetrust-accept-btn-handler"]').click()
                # page.get_by_role("button", name="OK").click()

                # select the link to click
                list_div_chapter = page.locator('div.drawer').all()
                for div_chapter in list_div_chapter:
                    chapter_header = div_chapter.locator('button')
                    chapter_header_text = chapter_header.inner_text()
                    chapter_header_text = chapter_header_text.strip()

                    print(chapter_header_text)


                    expanded = chapter_header.get_attribute('aria-expanded').strip()
                    expanded = expanded.lower()
                    if expanded == 'false':
                        print('click the chapter title')
                        div_chapter.click()

                    sections = div_chapter.locator('ul li').all()
                    for section in sections:
                        section_title = section.inner_text()
                        section_title = section_title.strip()
                        print('\tsection: {}'.format(section_title))

                        if section_title:
                            with page.expect_request(lambda request: True if re.match(r'.*\.html$', request.url) else False) as first:
                                section.click()

                            print('\tfirst url: {}'.format(first.value.url))
                            # page.wait_for_load_state('networkidle')
                            # page.wait_for_timeout(2000)

                            manual_page_meta_curr: ManualPageMeta = copy(manual_page_meta)
                            manual_page_meta_curr.chapter = chapter_header_text
                            manual_page_meta_curr.section = section_title

                            UtilityManualPageMeta.clean_chapter_section_title(manual_page_meta_curr)

                            path_html_curr, path_html_individual_curr = UtilityManualPageMeta.get_store_path(manual_page_meta_curr)

                            html_curr = page.content()
                            html_individual_url = first.value.url
                            html_individual = self.retrieve_html(context, html_individual_url)


                            manual_page_store_item = ManualPageStoreItem(**manual_page_meta_curr.model_dump(),
                                                                         path_html=path_html_curr,
                                                                         html=html_curr,
                                                                         path_html_individual=path_html_individual_curr,
                                                                         html_individual=html_individual,
                                                                         html_individual_url=html_individual_url)
                            page_collection.append(manual_page_store_item)


            except TimeoutError:
                logger.info('time out loading the page')
            except Exception as e:
                logger.info('error')
                logger.exception(e)
            finally:
                browser.close()
        return

    def retrieve_html(self, context: BrowserContext, url: str):
        page = context.new_page()
        html = ''
        try:
            timeout = CrawlManualHubpagePlaywright.default_timeout
            page.set_default_timeout(timeout)
            page.goto(url)

            html = page.content()
        except TimeoutError:
            print('time out loading the page')
        finally:
            page.close()
            return html

