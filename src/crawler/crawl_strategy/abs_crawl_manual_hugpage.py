#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

## @author: Bingqing

from abc import ABC, ABCMeta, abstractmethod
from pathlib import Path
from typing import List
from typing import Dict
import os
import io

from bs4 import BeautifulSoup

from crawler.data_structure.manual_page_meta import ManualPageMeta
from crawler.data_structure.manual_page_store_item import ManualPageStoreItem

import config.root_path as projRootPath

"""
Function:
    this is to hard code the crawling process of manual huge page
    Typically, a car model has a general hub page which allows the user
    to navigate through different topics. The content of ecah topic
    can be loaded by clicking the link in that hub page.
    To crawl the manual, we need to start from the hug page,
    follow the links to each topic, and eventually save the page that contain the
    topic presented.
    Different from a spyder that can walk randomly in the web,
    this customized crawler only propogate from parent hug page to child page in
    one or few levels.
##

"""
class AbsCrawlManualHubpage(ABC):


    @abstractmethod
    def crawl_all_subtopics(self, manual_page_meta: ManualPageMeta, page_collection: List[ManualPageStoreItem], crawl_param:Dict ):
        """
        Function: given hub page, crawl the sub topic page

        :param config_crawl_manual_job:
        :return:
        """
        pass

    def save_html_to_local_file(self, manual_page_store_item: ManualPageStoreItem, out_folder:Path):

        full_path_html = out_folder / manual_page_store_item.path_html
        full_path_html_individual = out_folder / manual_page_store_item.path_html_individual

        self.save_string_to_file(manual_page_store_item.html, full_path_html)
        self.save_string_to_file(manual_page_store_item.html_individual, full_path_html_individual)

        return

    def save_string_to_file(self, str_content, file_path:Path):
        if not file_path.parent.exists():
            os.makedirs(file_path.parent, exist_ok=True)


        with io.open(file_path, 'w', encoding='utf-8') as out:
            out.write(str_content)
            out.close()
            print('file saved: {}'.format(file_path))

        return

    def save_to_mongodb(self, manual_page_store_item: ManualPageStoreItem):
        return