
#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

import config.root_path as rp
class ImgPathUtil:

    @staticmethod
    def get_abs_path(rel_path:str):
        ret = rp.getRootPath() / rel_path
        return str(ret)