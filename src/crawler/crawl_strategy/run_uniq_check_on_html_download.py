#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

## @author: Bingqing Wang

import __future__
from pathlib import Path
from typing import List
import os
import io
import copy

import hydra
from omegaconf import DictConfig, OmegaConf

from bs4 import BeautifulSoup

import config.root_path as rp
from crawler.crawl_strategy.data_clean.car_manual.html_page_process_to_page import HtmlPageProcessToPage
from crawler.data_structure.doc_id_generator import DocIDGenerator
from crawler.data_structure.manual_page_store_item import UtilityManualPageStoreitem, ManualPageStoreItem
from crawler.data_structure.paragraph import Paragraph

from crawler.crawl_strategy.data_clean.car_manual.enum_data_clean_method import EnumDataCleanMethod
import crawler.crawl_strategy.data_clean.car_manual as dc



@hydra.main(version_base=None, config_path=str(rp.getRootPath()/'config'), config_name='config')
def main(cfg: DictConfig) -> None:


    # 1. load config
    cfg_job = cfg['data']['uniq_check']

    root_folder = rp.getRootPath()
    input_catalog_file = root_folder / cfg_job['input_catalog_file']
    html_folder = root_folder / cfg_job['input_html_folder']
    output_catalog_file = root_folder / cfg_job['output_catalog_file']

    item_list: List[ManualPageStoreItem] = UtilityManualPageStoreitem.load_from_json_file(input_catalog_file)

    id_uniq = set()
    uniq_item_list = list[ManualPageStoreItem]()
    duplicated_item_list = list[ManualPageStoreItem]()
    for item in item_list:
        id = DocIDGenerator.generate_id(item)
        if id not in id_uniq:
            id_uniq.add(id)
            uniq_item_list.append(item)
        else:
            duplicated_item_list.append(item)

    for item in duplicated_item_list:
        print(DocIDGenerator.generate_id(item))

    UtilityManualPageStoreitem.save_from_crawl_list_to_json_file_for_data_clean(uniq_item_list, output_catalog_file)

    return

if __name__ == '__main__':
    main()

