#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

## @author: Bingqing Wang

import __future__
import logging
from pathlib import Path
from typing import List
import os
import io
import copy



from bs4 import BeautifulSoup

import config.root_path as rp
from crawler.crawl_strategy.data_clean.car_manual.html_page_process_to_page import HtmlPageProcessToPage
from crawler.data_structure.doc_id_generator import DocIDGenerator
from crawler.data_structure.manual_page_store_item import UtilityManualPageStoreitem, ManualPageStoreItem

from crawler.crawl_strategy.data_clean.car_manual.enum_data_clean_method import EnumDataCleanMethod
import crawler.crawl_strategy.data_clean.car_manual as dc

logger = logging.getLogger(__name__)

class HtmlCleanManager:

    def __init__(self):
        pass

    def run(self,
            input_catalog_file:str,
            html_folder:str,
            outfile_path:str) -> None:

        # 1. get handler
        handler = dc.HtmlPageProcessToPage()

        # 2. process the html page
        input_collection: List[ManualPageStoreItem] = UtilityManualPageStoreitem.load_from_json_file(input_catalog_file)
        output_collection: List[ManualPageStoreItem] = []
        for in_mps_page in input_collection:
            path_html_individual = Path(html_folder) / Path(in_mps_page.path_html_individual)
            logger.info(f'path_html_individual: {path_html_individual}')
            new_mps_collection_per_item = handler.handle_mps(in_mps_page, str(html_folder))

            output_collection.extend(new_mps_collection_per_item)


        # 3. output result
        UtilityManualPageStoreitem.dump_list_for_index_construction(output_collection, str(outfile_path))

        cnt_input_files = len(input_collection)
        cnt_output_files = len(output_collection)

        logger.info(f'input total file: {cnt_input_files}')
        logger.info(f'output total file: {cnt_output_files}')

        return



