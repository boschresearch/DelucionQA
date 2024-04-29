#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

# this script is to load url list and crawl the page in batch

import __future__
import logging
from pathlib import Path
from typing import List, Dict
import os

from crawler.data_structure.manual_page_meta import ManualPageMeta, UtilityManualPageMeta
from crawler.data_structure.manual_page_store_item import UtilityManualPageStoreitem
from crawler.crawl_strategy.crawl_manual_hubpage_playwright import CrawlManualHubpagePlaywright
import config.root_path as rp


logger = logging.getLogger(__name__)

class CrawlManager:

    def __init__(self):
        pass


    def run_crawl_job(self, input_url_file:str, html_folder:str, catalog_json:str, crawl_param:Dict={}):
        job = CrawlManualHubpagePlaywright()

        total_mps_collection = []
        manual_page_meta_collection: List[ManualPageMeta] \
            = UtilityManualPageMeta.load_from_tab_file(input_url_file)

        logger.info('start crawling: ')
        html_folder_path = Path(html_folder)
        for mpm in manual_page_meta_collection:
            logger.info(f'current crawling url: {mpm.url}')
            try:
                mps_collection = []
                job.crawl_all_subtopics(mpm, mps_collection, crawl_param=crawl_param)
                for mps in mps_collection:
                    job.save_html_to_local_file(mps, html_folder_path)
                total_mps_collection.extend(mps_collection)
            except Exception as e:
                logger.warning(f'error in crawling the url: {mpm.url}')
                logger.exception(e)
            else:
                logger.info(f'{mpm.url} finished crawling')

        logger.info('dump out the meta info to json file as catalog file')
        UtilityManualPageStoreitem.save_from_crawl_list_to_json_file_for_data_clean(total_mps_collection, catalog_json)

        return

    def run_crawl_job_on_general_output(self, input_url_file: Path, output_folder: Path):
        html_folder = Path(output_folder) / "html"
        catalog_json = Path(output_folder) / 'html_file_list.json'

        self.run_crawl_job(input_url_file=input_url_file,
                           html_folder=html_folder,
                           catalog_json=catalog_json)

        return

    def run_crawl_job_maual_specified_url_complete(self):
        root_folder = rp.getRootPath()
        input_url_file = root_folder / 'data/crawl/url_list/manual_specified_collection_url.txt'
        output_folder = root_folder / 'data/crawl/manual_specified_collection/'
        os.makedirs(output_folder, exist_ok=True)

        self.run_crawl_job_on_general_output(input_url_file, output_folder)
        return

    def run_crawl_job_sample(self):
        root_folder = rp.getRootPath()
        input_url_file = root_folder / 'data/crawl/url_list/small_sample_url.txt'
        output_folder = root_folder / 'data/crawl/small_sample/'
        os.makedirs(output_folder, exist_ok=True)

        self.run_crawl_job_on_general_output(input_url_file, output_folder)
        return



if __name__ == '__main__':
    crawl_manager = CrawlManager()
    crawl_manager.run_crawl_job_sample()
    #run_crawl_job_maual_specified_url_complete()
