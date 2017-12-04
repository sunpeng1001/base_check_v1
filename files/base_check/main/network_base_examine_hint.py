# -*- coding: utf-8 -*-
import sys
sys.path.append("/tmp/base_check/")
from network_check.network_base_examine import *

if __name__ == '__main__':
    instance = Network_examine()
    print instance.network_device_check(target_net_device)
    print instance.network_device_state_check(target_net_device)
    print instance.network_device_mtu_check(target_net_device, target_net_device_mtu)
    print instance.network_device_speed_check(target_net_device, target_net_device_speed)
    print instance.network_device_mac_check(target_net_device)
    print instance.network_device_ipaddrss_check(target_net_device)
    print instance.network_device_connection_check(target_net_device)
    print instance.network_device_vlan_check(target_net_device)