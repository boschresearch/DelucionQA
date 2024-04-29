#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

## @author: Bingqing Wang

import __future__
from pathlib import Path
from typing import List
import os
import io

import requests

import hydra
from omegaconf import DictConfig, OmegaConf

from bs4 import BeautifulSoup
import config.root_path as rp
from crawler.data_structure.doc_id_generator import DocIDGenerator
from crawler.data_structure.manual_page_store_item import UtilityManualPageStoreitem, ManualPageStoreItem

from urllib.parse import urljoin, urlparse

@hydra.main(version_base=None, config_path=str(rp.getRootPath()/'config'), config_name='config')
def main(cfg: DictConfig):
    root_folder = rp.getRootPath()
    input_catalog_file = root_folder / 'data/crawl/manual_specified_collection/html_file_list.json'
    collection: List[ManualPageStoreItem] = UtilityManualPageStoreitem.load_from_json_file(input_catalog_file)

    html_folder = root_folder / 'data/crawl/manual_specified_collection/html/'

    img_folder = root_folder / 'data/img'

    img_src_collection = set()
    img_src_file = root_folder / 'data/crawl/img_src'
    cnt = 0
    limit = -1  # -1 to get all data parsed
    img_cnt = 0
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


            all_imgs = soup.find_all('img', src=True)
            for img in all_imgs:
                src = img['src']
                try:
                    parsed_url = urlparse(src)
                    if bool(parsed_url.netloc):

                        img_src_collection.add(src)
                        print(f'get image: {os.path.basename(parsed_url.path)}')
                        '''
                        img_data = requests.get(src).content
                        if img_data:
                            file_name = os.path.basename(parsed_url.path)
                            print(f'get image: {file_name}')
                            with open(img_folder / file_name, 'wb') as handler:
                                handler.write(img_data)
                                img_cnt = img_cnt + 1
                        '''
                except:
                    pass
                finally:
                    pass

            updated_html_content = soup.prettify()
            in_file.close()

        #with io.open(path_html_individual, 'w', encoding='utf-8') as out_file:
        #    if updated_html_content:
        #        out_file.write(updated_html_content)
        #    out_file.close()

        if limit > 0 and cnt >= limit:
            break

    with io.open(rp.getRootPath() / 'data/img_src', 'w') as out_file:
        for img_src in img_src_collection:
            out_file.write(img_src+"\n")
        out_file.close()
    print(f'total file: {cnt}')
    print(f'total image count: {img_cnt}')

    return

if __name__ == '__main__':
    main()

