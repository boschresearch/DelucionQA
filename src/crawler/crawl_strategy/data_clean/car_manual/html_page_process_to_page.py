#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0


import io
from copy import copy

from bs4 import BeautifulSoup

import config.root_path as rp
from crawler.crawl_strategy.data_clean.car_manual.abs_html_page_processor_car_manual import AbsHtmlPageProcessorCarManual
from crawler.data_structure.doc_id_generator import DocIDGenerator
from crawler.data_structure.manual_page_store_item import UtilityManualPageStoreitem, ManualPageStoreItem

class HtmlPageProcessToPage(AbsHtmlPageProcessorCarManual):

    def extract_content_from_html_file(self, path_html_individual:str) -> list:
        text = ''
        with io.open(path_html_individual, 'r', encoding='utf-8') as in_file:
            html_content = in_file.read()

            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text(separator='\n', strip=False)

            text = text.replace('\n', ' ')
            in_file.close()

        return [text]


    def create_mps_item(self, in_mps_page:ManualPageStoreItem, text) -> ManualPageStoreItem:
        item = copy(in_mps_page)
        item.id = DocIDGenerator.generate_id(in_mps_page)

        item.contents = text

        return item
