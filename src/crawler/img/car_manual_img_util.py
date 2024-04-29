#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

import os
from pathlib import Path
from urllib.parse import urlparse

import requests # to get image from the web
import shutil # to save it locally

import config.root_path as rp

class CarManualImgUtil:

    img_path= 'data/img/manual_specified_collection/'

    @staticmethod
    def crawl_url(url: str):
        try:
            url = url.strip()
            parsed_url = urlparse(url)
            r = None
            if bool(parsed_url.netloc):
                file_path = parsed_url.path
                dirname = os.path.dirname(file_path)
                basename = os.path.basename(file_path)

                dirname = CarManualImgUtil.img_path + "/" + dirname
                dirname = rp.getRootPath() / dirname
                if not Path(dirname).exists():
                    os.makedirs(dirname)

                r = requests.get(url, stream=True)

                if r.status_code == 200:
                    r.raw.decode_content = True
                    with open( dirname / basename, 'wb') as out_file:
                        shutil.copyfileobj(r.raw, out_file)
                        out_file.close()

                    print(f'{url} has been downloaded')
                else:
                    print(f'{url} cannot be retrieved')

                r.close()
        except Exception as e:
            print(e)
        finally:
            if r:
                r.close()

        return

    @staticmethod
    def get_file_path(url: str) -> Path:
        file_path = None
        try:
            url = url.strip()
            parsed_url = urlparse(url)
            if bool(parsed_url.netloc):
                file_path = CarManualImgUtil.img_path +  '/' + parsed_url.path

                file_path = rp.getRootPath() / file_path
                if not file_path.exists():
                    file_path = None
        except Exception as e:
            print(e)
        finally:
            return file_path
