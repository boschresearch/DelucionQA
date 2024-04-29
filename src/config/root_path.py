#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0

from pathlib import Path


def getRootPath() -> Path:
    return Path(__file__).parent.parent.parent
