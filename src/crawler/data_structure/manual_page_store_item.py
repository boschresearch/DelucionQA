#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

## @author Bingqing Wang
import os
import json
import io
from pathlib import Path
from typing import Optional, List, Set

import config.root_path as rp
from crawler.utility.io import FileUtil
from crawler.data_structure.manual_page_meta import ManualPageMeta


class ManualPageStoreItem(ManualPageMeta):
    #manual_page_meta: ManualPageMeta
    path_html: Optional[str] = None
    html: Optional[str] = None

    path_html_individual: Optional[str] = None
    html_individual: Optional[str] = None

    html_individual_url: Optional[str] = None
    contents: Optional[str] = None
    id: Optional[str] = None

    contents_type : Optional[str] = None
    contents_metadata : Optional[dict] = None

class UtilityManualPageStoreitem:

    @staticmethod
    def save_from_crawl_list_to_json_file_for_data_clean(itemList: List[ManualPageStoreItem], outfile: str):
        exclude_set = {"html", "html_individual", "contents", "id", "contents_type", "contents_metadata"}
        UtilityManualPageStoreitem._save_list_to_json_file(itemList, outfile, exclude_set)

        return

    @staticmethod
    def dump_list_for_index_construction(itemList: List[ManualPageStoreItem], outfile: str):
        exclude_set = {"html", "html_individual"}
        UtilityManualPageStoreitem._save_list_to_jsonl(itemList, outfile, exclude_set)

        return

    @staticmethod
    def _save_list_to_json_file(itemList: List[ManualPageStoreItem], outfile_path: str, exclude_set:Set[str]):
        print()
        out_dict_list = []
        for item in itemList:
            out_dict = item.model_dump(exclude=exclude_set)
            out_dict_list.append(out_dict)

        out_path = Path(outfile_path)
        if not out_path.parent.exists()  :
            os.makedirs(out_path.parent)

        with io.open(outfile_path, 'w', encoding='utf-8') as outfile:
            json.dump(out_dict_list, outfile, indent=4)
            outfile.close()

        print('job done')
        return

    @staticmethod
    def _save_list_to_jsonl(itemList: List[ManualPageStoreItem], outfile_path: str, exclude_set:Set[str]):

        out_dict_list = []
        for item in itemList:
            out_dict = item.model_dump(exclude=exclude_set)
            out_dict_list.append(out_dict)

        FileUtil.dump_dictList_to_jsonl(out_dict_list, outfile_path)
        return

    @staticmethod
    def load_from_json_file(infile_path: str) -> List[ManualPageStoreItem]:
        ret_list = list[ManualPageStoreItem]()
        with io.open(infile_path, 'r', encoding='utf-8') as infile:
            loaded_list = json.load(infile)
            if isinstance(loaded_list, List):
                for item_object in loaded_list:
                    model = ManualPageStoreItem(**item_object)
                    ret_list.append(model)
            infile.close()

        return ret_list

    @staticmethod
    def load_from_jsonl_file(infile_path:str) -> List[ManualPageStoreItem]:
        item_list = FileUtil.load_jsonl_file_to_dictList(infile_path)
        ret_list = []
        for item in item_list:
            model = ManualPageStoreItem(**item)
            ret_list.append(model)

        return ret_list

if __name__ == '__main__':
    data_jsonl = rp.getRootPath() / 'data/data_for_index/manual_specified_collection/doc_per_page/data.jsonl'
    print(data_jsonl)
    item_list = UtilityManualPageStoreitem.load_from_jsonl_file(str(data_jsonl))
    print(len(item_list))
    for item in item_list:
        print(item.path_html)
