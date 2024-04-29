
#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

from typing import Optional

from crawler.data_structure.manual_page_store_item import ManualPageStoreItem

class ManualPageStoreItemExtPageSeg(ManualPageStoreItem):
    fig_abs_url: Optional[str] = None
    title_chain: Optional[str] = None
    logic_level: Optional[int] = None
    segment_logic_level: Optional[int] = None

