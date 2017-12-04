# -*- coding: utf-8 -*-
import csv
import os
import re
import sys
sys.path.append("/tmp/base_check/")
from conf.base_conf import manager_ip_address
from conf.base_conf import mac_check_data_file

device_list = os.listdir('/sys/class/net/')
list = manager_ip_address.split('.', 4)
list[2] = str(int(list[2]) + 3)
ipmi_address = '.'.join(list)
#This class only can examine network device mac
# which is unbonded or bond one or two network devices.

class Network_device_mac_examine():
    device_list = os.listdir('/sys/class/net/')

    def mac_check(self,host=ipmi_address):
        with open(mac_check_data_file,'rb') as f:
            read = csv.DictReader(f)
            for row in read:
                if row['IPMI'] == host:
                    mac_list = []
                    device_list_file = []
                    for i in row.keys():
                        if i != 'IPMI':
                            device_list_file.append(i)
                            mac_list.append(row[i])
                    return dict(zip(device_list_file,mac_list))

    def get_network_device_mac(self,device):
        os.environ['device'] = device
        bond_device_bool = os.popen("ip -o link|grep $device |grep master&>/dev/null;echo $?").read()
        if device in Network_device_mac_examine.device_list and int(bond_device_bool) == 0:
            bond_master = os.popen("ip -o link|grep $device |grep master|awk '{print $9}'").read()
            os.environ['bond_master'] = bond_master.strip()
            slave_bool = os.popen("cat /proc/net/bonding/$bond_master |grep -C 5 $device|grep Permanent|wc -l").read()
            if int(slave_bool) == 2:
                slave_device_mac = os.popen("cat /proc/net/bonding/$bond_master|"
                                            "grep -C 5  $device|grep Permanent|awk NR==2|awk '{print $4}'").read()
                return slave_device_mac.strip()
            else:
                slave_device_mac = os.popen("cat /proc/net/bonding/$bond_master|"
                                             "grep -C 5 $device|grep Permanent|awk '{print $4}'").read()
                return slave_device_mac.strip()
        elif device in Network_device_mac_examine.device_list and int(bond_device_bool) != 0:
            device_mac = os.popen("cat /sys/class/net/$device/address").read()
            return device_mac.strip()
        else:
            return None

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
