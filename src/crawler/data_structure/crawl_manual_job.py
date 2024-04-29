#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

## @author Bingqing Wang
from pathlib import Path

from pydantic import BaseModel

from crawler.data_structure.manual_page_meta import ManualPageMeta

class CrawlManualJob(BaseModel):
    hubpage_url: str
    root_output_path: str
    url_to_dump_folder_name = 'url_to_dump_folder_name'
    root_html_dump_folder = 'html_dump'
    link_graph_file_name = 'link_graph'

