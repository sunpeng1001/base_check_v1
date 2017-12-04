# -*- coding: utf-8 -*-
import sys
sys.path.append("/tmp/base_check/")
from network_check.network_bond_examine import *

if __name__ == '__main__':
    instance = Network_device_bond_examine()
    print instance.network_device_check(target_net_device)
    print instance.network_device_bond_check(target_net_device)