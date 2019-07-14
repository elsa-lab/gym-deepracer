import os
import sys
import time
import logging

import multiprocessing


UNIVERSAL_LOCK = multiprocessing.Value('i', 0)
