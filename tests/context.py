"""
This module helps us test without having to install the package"""

import os
import sys

addpath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, addpath)

import stingeripc
