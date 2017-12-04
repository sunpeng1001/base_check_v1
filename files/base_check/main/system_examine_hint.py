# -*- coding: utf-8 -*-
import sys
sys.path.append("/tmp/base_check/")
from system_check.system_examine import *

if __name__ == '__main__':
    instance = System_examine()
    print instance.tcp_and_udp_port_check()