# -*- coding: utf-8 -*-
import os
import csv
import sys
sys.path.append("/tmp/base_check/")
from conf.base_conf import manager_ip_address
from conf.base_conf import cpu_vendor_conf
from conf.base_conf import cpu_socket_num_conf
from conf.base_conf import cpu_cores_per_socket_conf
from conf.base_conf import cpu_threads_per_core_conf
from conf.base_conf import cpu_check_data_file

class CPU_examine():
    list = manager_ip_address.split('.',4)
    list[2] = str(int(list[2]) + 4)
    ipmi_address = '.'.join(list)
    def cpu_base_check(self):
        target_node_cpuinfo = os.popen("lscpu|grep 'Model name'|awk -F 'CPU' '{print $2}'").read()
        CPU_conf = 'CPU_CONF:None'
        cpu_vendor = os.popen("lscpu|grep 'Model name'|awk -F ':' '{print $2}'|awk '{print $1}'").read()
        cpu_socket_num = os.popen("lscpu|grep 'Socket(s)'|awk -F ':' '{print $2}'").read()
        cpu_cores_per_socket = os.popen("lscpu|grep 'Core(s)'|awk -F ':' '{print $2}'").read()
        cpu_threads_per_core = os.popen("lscpu|grep 'Thread(s)'|awk -F ':' '{print $2}'").read()

        with open(cpu_check_data_file, 'rb') as f:
            read = csv.DictReader(f)
            for row in read:
                if row['IPMI'] == CPU_examine.ipmi_address:
                    cpu_conf = row['cpu']
                    if cpu_conf.find(target_node_cpuinfo):
                        CPU_conf = 'CPU_CONF:%s' %target_node_cpuinfo.strip('\n')
                    else:
                        CPU_conf = 'CPU_CONF:Error(%s)' %target_node_cpuinfo.strip('\n')
                else:
                    pass

        if cpu_vendor.strip('\n').find(cpu_vendor_conf) == 0:
            cpu_vender_info = 'CPU_Vendor:%s' %cpu_vendor.strip().strip('(R)')
        else:
            cpu_vender_info = 'CPU_Vendor:Error(%s)' %cpu_vendor.strip().strip('(R)')


        if cpu_socket_num_conf == int(cpu_socket_num):
            cpu_socket_num_info = 'Sockets:%s' %int(cpu_socket_num)
        else:
            cpu_socket_num_info = 'Sockets:Error(%s)' %int(cpu_socket_num)


        if cpu_cores_per_socket_conf == int(cpu_cores_per_socket):
            cores_per_socket_info = 'Cores_Per_Socket:%s' %int(cpu_cores_per_socket)
        else:
            cores_per_socket_info = 'Cores_Per_Socket:Error(%s)' %int(cpu_cores_per_socket)

        if cpu_threads_per_core_conf == int(cpu_threads_per_core):
            cpu_threads_per_core_info = 'Threads_Per_Core:%s' %int(cpu_threads_per_core)
        else:
            cpu_threads_per_core_info = 'Threads_Per_Core:Error(%s)' %int(cpu_threads_per_core)

        return cpu_vender_info,CPU_conf,cpu_socket_num_info,cores_per_socket_info,cpu_threads_per_core_info


if __name__ == '__main__':
    a = CPU_examine()
    print a.cpu_base_check()

