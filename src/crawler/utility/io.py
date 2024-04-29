#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

from __future__ import annotations

import logging
import os
from pathlib import Path
import io
import json
from typing import List

from pydantic import BaseModel
from tqdm import tqdm

from typing import Counter, Set


import config.root_path as rp

class FileUtil:

    logger = logging.getLogger("FileUtil")

    @staticmethod
    def dump_dictList_to_jsonl(out_dict_list:List[dict], outfile_path:str, use_tqdm=False):
        logger = logging.getLogger('utility.io.FileUtil.dump_dictList_to_jsonl')

        logger.info('Start')

        os.makedirs(Path(outfile_path).parent, exist_ok=True)
        with io.open(outfile_path, 'w', encoding='utf-8') as outfile:
            iter = tqdm(out_dict_list) if use_tqdm else out_dict_list
            for item in iter:
                json.dump(item, outfile)
                outfile.write('\n')

            outfile.close()

        logger.info('Done')

        return

    @staticmethod
    def load_jsonl_file_to_dictList(infile_path: str) -> List[dict]:
        ret_list = list[dict]()
        with io.open(infile_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
            for line in lines:
                item = json.loads(line)
                ret_list.append(item)

            infile.close()

        return ret_list


    @staticmethod
    def load_list_of_lines(infile_path: str) -> List[str]:
        ret_list = []
        with io.open(infile_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
            ret_list.extend(lines)
            infile.close()

        return ret_list

    @staticmethod
    def dump_counter_to_file(counter: Counter, outfile_path: str, use_tqdm=False):

        FileUtil.logger.info('Start')

        os.makedirs(Path(outfile_path).parent, exist_ok=True)
        with io.open(outfile_path, 'w', encoding='utf-8') as outfile:
            iter = tqdm(counter.items()) if use_tqdm else counter.items()
            for k, v in iter:
                outfile.write(f'{v}\t{k}\n')

            outfile.close()

        FileUtil.logger.info('Done')

        return

    @staticmethod
    def save_list_to_json_file(itemList: List[BaseModel], outfile_path: str, exclude_set: Set[str]):
        try:
            msg = f'save to file: {outfile_path}'
            FileUtil.logger.warning(msg)
            out_dict_list = []
            for item in itemList:
                out_dict = item.dict(exclude=exclude_set)
                out_dict_list.append(out_dict)

            with io.open(outfile_path, 'w', encoding='utf-8') as outfile:
                json.dump(out_dict_list, outfile, indent=4)
                outfile.close()

        except Exception as e:
            print(e)
            FileUtil.logger.exception(e)
        else:
            FileUtil.logger.warning("job done")

        return

    @staticmethod
    def save_list_to_jsonl(itemList: list, outfile_path: str, exclude_set: Set[str]):

        out_dict_list = []
        for item in itemList:
            out_dict = item.dict(exclude=exclude_set)
            out_dict_list.append(out_dict)

        FileUtil.dump_dictList_to_jsonl(out_dict_list, outfile_path)
        return

    @staticmethod
    def load_from_json_file(infile_path: str) -> list:
        ret_list = list()
        with io.open(infile_path, 'r', encoding='utf-8') as infile:
            loaded_list = json.load(infile)
            if isinstance(loaded_list, List):
                for item_object in loaded_list:
                    ret_list.append(item_object)
            infile.close()

        return ret_list

    @staticmethod
    def load_json_files_from_folder(folder: str) -> list:
        ret_list = []
        if os.path.exists(folder) and os.path.isdir(folder):
            files = os.listdir(folder)

            for file in files:
                full_path = folder + '/' + file
                if os.path.isfile(full_path):
                    items = FileUtil.load_from_json_file(full_path)
                    ret_list.extend(items)

        return ret_list


    @staticmethod
    def load_from_jsonl_file(infile_path: str) -> list:
        item_list = FileUtil.load_jsonl_file_to_dictList(infile_path)
        ret_list = []
        for item in item_list:
            ret_list.append(item)

        return ret_list

    @staticmethod
    def makedirs_under_proj_dir(rel_path, bool_is_file:bool=True):
        abs_path = rp.getRootPath() / rel_path
        if bool_is_file:
            abs_path_dir = os.path.dirname(abs_path)
            os.makedirs(abs_path_dir, exist_ok=True)
        else:
            os.makedirs(abs_path, exist_ok=True)
        return

    @staticmethod
    def makedirs_for_abs_dir(abs_path, bool_is_file: bool = True):

        if bool_is_file:
            abs_path_dir = os.path.dirname(abs_path)
            os.makedirs(abs_path_dir, exist_ok=True)
        else:
            os.makedirs(abs_path, exist_ok=True)
        return

    @staticmethod
    def load_file_str(abs_file_path:str):
        str = ''
        with open(abs_file_path, 'r') as file:
            str = file.read()
            file.close()

        return str