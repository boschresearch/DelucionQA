#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

# Created by wab2pal at 12/19/23

# This class is to control the process of crawling and data processing
import logging
from pathlib import Path
from typing import List, Dict

from crawler.crawl_strategy.crawl_manager import CrawlManager
from crawler.crawl_strategy.html_clean_manager import HtmlCleanManager

import config.root_path as rp

logger = logging.getLogger(__name__)

class JobManager:

    def __init__(self, input_url_file:str, output_folder:str):
        self.input_url_file = str(rp.getRootPath() / input_url_file)
        self.output_folder = str(rp.getRootPath() / output_folder)

        self.crawl_manager = CrawlManager()
        self.html_clean_manager = HtmlCleanManager()
        return


    def run(self, crawl_param:Dict={}):
        catalog_json = self.output_folder + '/' + 'catalog.json'
        html_folder = self.output_folder + '/' + 'html'

        self.crawl_manager.run_crawl_job(input_url_file=self.input_url_file,
                                         catalog_json=catalog_json,
                                         html_folder=html_folder,
                                         crawl_param=crawl_param)

        outfile_path = self.output_folder + '/' + 'data.jsonl'

        self.html_clean_manager.run(input_catalog_file=catalog_json,
                                    html_folder=html_folder,
                                    outfile_path=outfile_path)
        return
