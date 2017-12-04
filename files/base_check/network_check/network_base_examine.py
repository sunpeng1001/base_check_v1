# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("/tmp/base_check/")
from conf.base_conf import target_net_device
from conf.base_conf import target_net_device_mtu
from conf.base_conf import target_net_device_speed
from conf.base_conf import target_net_gateway

class Network_examine():
    target_network_device_var = os.listdir('/sys/class/net/')
    os.environ['target_device'] = target_net_device
    os.environ['target_network_gateway'] = target_net_gateway

    def network_device_check(self,target_network_device):
        if target_network_device in Network_examine.target_network_device_var:
            target_network_device =  target_net_device
            return ('Name:%s' %(target_network_device))
        else:
            return ("Name:None")

    def network_device_state_check(self,target_network_device):
        if target_network_device in Network_examine.target_network_device_var:
            target_network_device_state_var = os.popen("cat /sys/class/net/$target_device/operstate").read()
            if target_network_device_state_var.strip('\n') == 'up':
                return ('State:UP')
            else:
                return ('State:DOWN')
        else:
            return ('State:None')

    def network_device_mtu_check(self,target_network_device,target_network_mtu):
        if target_network_device in Network_examine.target_network_device_var:
            target_network_device_mtu_var = os.popen("cat /sys/class/net/$target_device/mtu").read()
            if target_network_mtu == int(target_network_device_mtu_var):
                return ('MTU:%s'  %int(target_network_device_mtu_var))
            else:
                return ('MTU:Error')
        else:
            return ('MTU:None')

    def network_device_speed_check(self,target_network_device,target_network_speed):
        if target_network_device in Network_examine.target_network_device_var:
            target_network_device_speed_var = os.popen("cat /sys/class/net/$target_device/speed").read()
            if target_network_speed == int(target_network_device_speed_var):
                return ('Speed:%s'%int(target_network_device_speed_var))
            else:
                return ('Speed:Error')
        else:
            return ('Speed:None')

    def network_device_mac_check(self,target_network_device):
        if target_network_device in Network_examine.target_network_device_var:
            target_network_device_mac_var = os.popen("cat /sys/class/net/$target_device/address").read()
            return ('MAC:%s' %(target_network_device_mac_var).strip('\n'))
        else:
            return ('MAC:None')

    def network_device_ipaddrss_check(self,target_network_device):
        if target_network_device in Network_examine.target_network_device_var:
            target_device_ipaddress = os.popen("ip -o a|grep $target_device|awk NR==1|grep -w inet|awk '{print $4}'").read()
            if target_device_ipaddress:
                return ('IP:%s' %target_device_ipaddress.strip('\n'))
            else:
                return ('IP:None')
        else:
            return ('IP:None')

    def network_device_connection_check(self,target_network_device):
        if target_network_device in Network_examine.target_network_device_var:
            target_device_connection = os.popen("ping -I $target_device -c 1 $target_network_gateway&>/dev/null;echo $?").read()
            if int(target_device_connection) == 0:
                return ('Connection:OK')
            else:
                return ('Connection:Error')
        else:
            return ('Connection:None')

    def network_device_vlan_check(self,target_network_device):
        if target_network_device in Network_examine.target_network_device_var:
            if os.path.exists('/proc/net/vlan'):
                target_network_vlan_device = os.listdir('/proc/net/vlan')
                if target_net_device in target_network_vlan_device:
                    vlan_id = os.popen("cat /proc/net/vlan/config|grep -w $target_device |awk '{print $3}'").read()
                return ('VLAN:%s'%vlan_id.strip('\n'))
            else:
                return ('VLAN:None')
        else:
            return ('VLAN:None')

if __name__ == "__main__":
    a = Network_examine()
    print a.network_device_check(target_net_device)
    print a.network_device_state_check(target_net_device)
    print a.network_device_mtu_check(target_net_device,target_net_device_mtu)
    print a.network_device_speed_check(target_net_device,target_net_device_speed)
    print a.network_device_mac_check(target_net_device)
    print a.network_device_ipaddrss_check(target_net_device)
    print a.network_device_connection_check(target_net_device)
    print a.network_device_vlan_check(target_net_device)