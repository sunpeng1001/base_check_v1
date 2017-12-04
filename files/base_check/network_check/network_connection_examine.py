# -*- coding: utf-8 -*-
import os
import sys
import threading
import time

sys.path.append("/tmp/base_check/")
from conf.base_conf import target_devices
from conf.base_conf import ping_test_duration
from conf.base_conf import ping_test_timeout
import pdb


test_device_count = len(target_devices)
exec_path = '/tmp'
os.environ['exec_path'] = exec_path
os.environ['ping_duration'] = ping_test_duration
network_device_list = os.listdir('/sys/class/net/')
network_device_list_conf = []

def network_device_check():
    for device in target_devices:
        network_device_list_conf.append(device['name'])
    if set(network_device_list_conf) & set(network_device_list) == set(network_device_list_conf):
        return 0
    else:
        return 1

def network_connnection_check():
    for device in target_devices:
        os.environ['var1'] = device['name']
        os.environ['var2'] = device['gateway']
        t = threading.Thread(target=ping_check)
        t.start()
        time.sleep(1)

def ping_check():
    os.system("ping -I $var1 $var2 -i 0.01 -w $ping_duration >$exec_path/$var1.txt ")

def check_result():
    for device in target_devices:
        os.environ['var1'] = device['name']
        var1=os.popen("cat $exec_path/$var1.txt |grep transmitted|awk '{print $1}'").read()
        var2=os.popen("cat $exec_path/$var1.txt |grep transmitted|awk '{print $4}'").read()
        loss_num = int(var1) - int(var2)
        loss_percent = (float(loss_num)/float(var1))
        if int(var1) == int(var2) or loss_percent < 0.0005:
            print ('%s:OK(%d)'%(device['name'],loss_num))
        elif int(var2) == 0:
            print ('%s:Unreachable'%device['name'])
        else:
            print ('%s:Error(%d/%d/%f)'%(device['name'],int(var1),loss_num,loss_percent))

def test_file_delete():
    for device in target_devices:
        test_file = exec_path +'/' + device['name'] + '.txt'
        os.remove(test_file)

if __name__ == "__main__":
#    pdb.set_trace()
    if network_device_check() == 0:
        network_connnection_check()
        result_num = os.popen("grep transmitted $exec_path/*.txt|wc -l").read()
        second = 0
        while int(result_num) != int(test_device_count):
            result_num = os.popen("grep transmitted $exec_path/*.txt|wc -l").read()
            time.sleep(1)
            second = second + 1
            if second == ping_test_timeout:
                print("Timeout!")
                break
        else:
             check_result()
        test_file_delete()
    else:
        print('Device:Error')
