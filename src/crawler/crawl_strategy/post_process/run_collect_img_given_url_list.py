
#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

import io
import hydra
from hydra import compose, initialize_config_dir as init_config_dir
from omegaconf import OmegaConf, DictConfig

import config.root_path as rp
from crawler.img.car_manual_img_util import CarManualImgUtil

@hydra.main(version_base=None, config_path=str(rp.getRootPath()/'config'), config_name='config')
def main(cfg: DictConfig):
    input_img_url_list_file = 'img_src'
    input_img_url_list_file = rp.getRootPath() / 'data/crawl' / input_img_url_list_file

    limit = -1
    with io.open(input_img_url_list_file, 'r', encoding='utf-8') as in_file:
        urls = in_file.readlines()
        cnt = 0
        for url in urls:
            CarManualImgUtil.crawl_url(url)
            cnt = cnt + 1
            if limit > 0 and cnt >= limit:
                break
        in_file.close()

    return

if __name__ == '__main__':
    main()