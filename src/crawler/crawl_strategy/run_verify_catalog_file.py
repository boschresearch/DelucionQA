#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

import __future__
from pathlib import Path
from typing import List
import os

import config.root_path as rp
from crawler.data_structure.manual_page_store_item import UtilityManualPageStoreitem, ManualPageStoreItem


def main():
    root_folder = rp.getRootPath()
    input_catalog_file = root_folder / 'data/crawl/manual_specified_collection/html_file_list.json'
    collection: List[ManualPageStoreItem] = UtilityManualPageStoreitem.load_from_json_file(input_catalog_file)

    html_folder = root_folder / 'data/crawl/manual_specified_collection/html/'
    cnt = 0
    for item in collection:
        path_html_individual = html_folder/ Path(item.path_html_individual)
        if not path_html_individual.exists():
            print("path exist: {}  {}".format(path_html_individual.exists(), path_html_individual))
        cnt = cnt + 1

    print(f'total file: {cnt}')

    return


if __name__ == '__main__':
    main()