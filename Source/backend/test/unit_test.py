import re
import os
import sys
import glob
import math
import copy
import unittest

from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 설정파일
load_dotenv()

# path 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api.utils.data_util import *


class UnitTest(unittest.TestCase):
    # @unittest.skip
    def test_1(self):
        pass

    @unittest.skip
    def test_0(self):
        path = os.getenv("PATH_NAS_ROOT")
        print("path:", path)


if __name__ == "__main__":
    unittest.main()
