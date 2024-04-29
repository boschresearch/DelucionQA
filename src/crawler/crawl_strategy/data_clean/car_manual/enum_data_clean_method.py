#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

from enum import Enum

class EnumDataCleanMethod(Enum):
    html_to_page = 0
    html_to_paragraph = 1
    html_to_topdown_sliding_window_dynamic = 3
    html_to_topdown_subsection = 4