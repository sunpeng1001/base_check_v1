# -*- coding: utf-8 -*-
import sys
sys.path.append("/tmp/base_check/")
from network_check.network_device_mac_examine import *

if __name__ == '__main__':
    a = Network_device_mac_examine()
    server_device_mac_file_list = a.mac_check()
    mac_list = []
    network_device_list = []
    for i in device_list:
        if i != 'bonding_masters' and (not re.match( r'(.*)bond(.*)', i)):
            network_device_list.append(i)
            mac_list.append(a.get_network_device_mac(i))
    server_device_mac_list = dict(zip(network_device_list,mac_list))
    for device in server_device_mac_file_list.keys()[::-1]:
        server_mac = a.get_network_device_mac(device)
        if server_mac == server_device_mac_file_list[device].lower():
            print '%s:OK' %device
        elif device not in device_list:
            print '%s:%s' %(device,server_mac)
        elif server_device_mac_file_list[device] =='':
            print '%s:%s'%(device,server_mac)
        else:
            print '%s:Error' %device
