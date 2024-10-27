
import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def dread_path():
    return Path(os.environ["DREAD_PATH"])
