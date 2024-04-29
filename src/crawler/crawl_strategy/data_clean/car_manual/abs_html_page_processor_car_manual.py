#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from typing import List

from crawler.data_structure.manual_page_store_item import ManualPageStoreItem

class AbsHtmlPageProcessorCarManual(ABC):

    def handle_mps(self, in_mps_page: ManualPageStoreItem, input_html_root_folder:str) -> List[ManualPageStoreItem]:
        ret_mps_collection = []
        path_html_individual = input_html_root_folder + '/' + in_mps_page.path_html_individual
        content_list = self.extract_content_from_html_file(path_html_individual)
        for content in content_list:
            content_mps_item:ManualPageStoreItem = self.create_mps_item(in_mps_page, content)
            ret_mps_collection.append(content_mps_item)

        return ret_mps_collection

    @abstractmethod
    def extract_content_from_html_file(self, path_html_individual) -> list:
        pass

    @abstractmethod
    def create_mps_item(self, in_mps_page:ManualPageStoreItem, content) -> ManualPageStoreItem:
        pass
