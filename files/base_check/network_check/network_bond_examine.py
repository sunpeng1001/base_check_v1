# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("/tmp/base_check/")
from network_base_examine import Network_examine
from conf.base_conf import target_net_device

class Network_device_bond_examine(Network_examine):
    target_network_device_var = os.listdir('/sys/class/net/')
    os.environ['target_device'] = target_net_device
    def network_device_bond_check(self,target_network_device):
        if target_network_device in Network_device_bond_examine.target_network_device_var:
            if os.path.exists('/proc/net/bonding'):
                target_network_bond_device = os.listdir('/proc/net/bonding')
                if target_network_device in target_network_bond_device:
                    bonding_mode = os.popen("cat /proc/net/bonding/$target_device|grep 'Bonding Mode'|awk '{print $5}'").read()
                    bonding_slaves = os.popen("cat /proc/net/bonding/$target_device|grep 'Slave Interface'|awk '{print $3}'").read()
                    os.environ['var'] = bonding_slaves
                    bonding_slaves_state = os.popen("for i in $var ;do cat /sys/class/net/$i/operstate;done").read()
                    bonding_slaves_speed = os.popen("for i in $var ;do cat /sys/class/net/$i/speed;done").read()
                    return ('Bond:YES Bond_Mode:%s  Bond_slave:%s  State:%s  Speed:%s'
                          %(bonding_mode,bonding_slaves,bonding_slaves_state,bonding_slaves_speed))
                else:
                    return ('Bond:NO  Bond_Mode:None  Bond_slaves:None  State:None  Speed:None')
            else:
                return ('Bond:NO  Bond_Mode:None  Bond_slave:None  State:None  Speed:None')
        else:
            return ('Bond:None Bond_mode:None  Bond_slave:None  State:None  Speed:None')

if __name__ == '__main__':
    a = Network_device_bond_examine()
    print a.network_device_check(target_net_device)
    print a.network_device_bond_check(target_net_device)
