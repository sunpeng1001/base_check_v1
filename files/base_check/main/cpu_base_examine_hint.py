# -*- coding: utf-8 -*-
import sys
sys.path.append("/tmp/base_check/")
from cpu_check.cpu_base_examine import *

if __name__ == '__main__':
    a = CPU_examine()
    for i in a.cpu_base_check():
       print i
