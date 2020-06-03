import os
import sys

proj_dir = os.path.join(os.path.dirname(__file__), '..')
proj_dir = os.path.abspath(proj_dir)
sys.path.insert(0, proj_dir)

import data
import utils
