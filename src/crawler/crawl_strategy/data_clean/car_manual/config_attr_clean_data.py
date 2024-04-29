#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

from __future__ import annotations

from enum import Enum
from strenum import StrEnum

class SegmentStyle(StrEnum):
    mix = 'mix'
    unmix = 'unmix'


class ConfigAttrCleanData(Enum):
    subsection_level = 0
    segment_style = SegmentStyle.mix



