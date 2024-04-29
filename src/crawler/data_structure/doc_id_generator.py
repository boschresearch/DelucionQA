
#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

import re
from crawler.data_structure.manual_page_store_item import ManualPageStoreItem

class DocIDGenerator:

    @staticmethod
    def generate_id(item: ManualPageStoreItem):
        id = f'{item.car_brand}-{item.car_model}-{item.year}-{item.chapter}-{item.section}'
        id = re.sub(r"\s+", '_', id)
        return id