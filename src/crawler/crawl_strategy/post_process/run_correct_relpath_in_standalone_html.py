#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

## @author: Bingqing Wang

import __future__
from pathlib import Path
from typing import List
import os
import io

from bs4 import BeautifulSoup
import config.root_path as rp
from crawler.crawl_strategy.post_process.html_relpath_converter import HtmlRelpathConverter
from crawler.data_structure.doc_id_generator import DocIDGenerator
from crawler.data_structure.manual_page_store_item import UtilityManualPageStoreitem, ManualPageStoreItem

from urllib.parse import urljoin, urlparse

def main():
    root_folder = rp.getRootPath()
    input_catalog_file = root_folder / 'data/crawl/manual_specified_collection/html_file_list.json'
    collection: List[ManualPageStoreItem] = UtilityManualPageStoreitem.load_from_json_file(input_catalog_file)

    html_folder = root_folder / 'data/crawl/manual_specified_collection/html/'
    cnt = 0
    limit = -1  # -1 to get all data parsed
    for item in collection:
        path_html_individual = html_folder / Path(item.path_html_individual)
        base_url = ''

        cnt = cnt + 1
        if r'hub.html' in str(item.path_html_individual):
            print('no operation')
            continue
        else:
            base_url = item.html_individual_url if item.html_individual_url else ''

        print(path_html_individual)

        updated_html_content = ''
        with io.open(path_html_individual, 'r', encoding='utf-8') as in_file:
            html_content = in_file.read()
            updated_html_content = html_content

            soup = BeautifulSoup(html_content, 'html.parser')
            HtmlRelpathConverter.handle(soup, base_url)
            updated_html_content = soup.prettify()
            in_file.close()

        with io.open(path_html_individual, 'w', encoding='utf-8') as out_file:
            if updated_html_content:
                out_file.write(updated_html_content)
            out_file.close()

        if limit > 0 and cnt >= limit:
            break

    print(f'total file: {cnt}')

    return

if __name__ == '__main__':
    main()

