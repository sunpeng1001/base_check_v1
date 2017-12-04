# -*- coding: utf-8 -*-
import os
import time
import threading
import sys
import pdb
sys.path.append("/tmp/base_check/")
from conf.base_conf import test_cluster_host
from conf.base_conf import manager_ip_address
from conf.base_conf import check_time

local_ip_list = []
local_device_list = []
device_list = os.listdir('/sys/class/net/')

class Network_speed_test_examine():


    def device_ipaddr_check(self,device_name):
        os.environ['device_name'] = device_name
        device_which_has_ipaddr = os.popen("ip -o -4 a |awk '{print $2}'").read().strip().split('\n')

        if os.path.exists("/proc/net/bonding"):
            bonding_slave = os.popen("cat /proc/net/bonding/*|grep 'Slave Interface'|awk '{print $3}'").read().strip().split()
            if device_name in bonding_slave or device_name not in device_which_has_ipaddr:
                device_ipaddr = ''
            else:
                device_ipaddr = os.popen("ip -o -4 a |grep $device_name|awk NR==1|awk '{print $4}'").read()
        elif not os.path.exists("/proc/net/bonding") and device_name in device_which_has_ipaddr:
            device_ipaddr = os.popen("ip -o -4 a |grep $device_name|awk NR==1|awk '{print $4}'").read()
        else:
            device_ipaddr = ''
        return device_ipaddr


    def firewalld_service_stop(self):
        firewalld_service_state = os.popen("systemctl status firewalld|grep -w active|awk '{print $2}'").read()
        if firewalld_service_state.strip() == 'active':
            os.system("systemctl stop firewalld")
            return 0
        else:
            return 1


    def firewalld_service_start(self):
        os.system("systemctl start firewalld")


    def device_iperf_server_check(self,local_ip):
        os.environ['local_ip'] = local_ip
        os.system("iperf -s -B $local_ip &>/tmp/$local_ip.txt &")


    def device_iperf_clinet_check(self,targert_ip,check_time):
        device_ipaddr_str = "iperf -c %s -t %d &>/dev/null&" %(targert_ip,check_time)
        os.system(device_ipaddr_str)


    def kill_iperf_server(self):
        os.system("for i in $(pidof iperf);do kill -9 $i;done")


    def iperf_server_client_num_check(self,device_name):
        instance = Network_speed_test_examine()
        device_ipaddr = instance.device_ipaddr_check(device_name)
        if device_ipaddr == '':
            client_num = 0
        else:
            device_ipaddr = device_ipaddr.replace('/24\n', '')
            device_ipaddr_str = "cat /tmp/%s.txt |grep connected|awk '{print $9}'|sort|uniq|wc -l" % device_ipaddr.strip()
            client_num = os.popen(device_ipaddr_str).read()
        return int(client_num)


    def get_device_conf_speed(self,device_name):
        device_speed_str = "cat /sys/class/net/%s/speed" %device_name
        device_speed = os.popen(device_speed_str).read()
        return int(device_speed)

    def network_device_receive_flow_check(self,device_name,check_time):
        instance =  Network_speed_test_examine()
        device_speed = instance.get_device_conf_speed(device_name)
        eligible_speed = device_speed * 0.8
        device_name_str = "cat /proc/net/dev | grep %s | awk '{print $2}'" %device_name
        device_receive_flow_init = os.popen(device_name_str).read()
        time.sleep(check_time)
        device_receive_flow_ult = os.popen(device_name_str).read()
        device_receive_flow = ((int(device_receive_flow_ult) - int(device_receive_flow_init))/check_time)*8
        client_num = instance.iperf_server_client_num_check(device_name)
        if device_receive_flow < 1024:
            device_receive_flow = device_receive_flow
            print '%s:Error(%db/s[%d])' %(device_name,device_receive_flow,client_num)
        elif device_receive_flow >= 1024 and device_receive_flow < 1048576:
            device_receive_flow = device_receive_flow / 1024
            print '%s:Error(%dKb/s[%d])' % (device_name, device_receive_flow,client_num)
        elif device_receive_flow >= 1048576  and device_receive_flow < 1073741824:
            device_receive_flow = device_receive_flow / 1048576
            if device_receive_flow <= eligible_speed:
                print '%s:Error(%dMb/s[%d])' % (device_name, device_receive_flow,client_num)
            else:
                print '%s:%dMb/s(%d)' % (device_name, device_receive_flow, client_num)
        else:
            device_receive_flow = round(float(device_receive_flow) / 1073741824.0,1)
            if device_receive_flow <= (eligible_speed/1000)*0.8:
                print '%s:Error(%.1fGb/s[%d])' % (device_name, device_receive_flow,client_num)
            else:
                print '%s:%.1fGb/s(%d)' % (device_name, device_receive_flow,client_num)


    def network_device_transmit_flow_check(self,device_name,check_time):
        pass


    def test_file_delete(self,ip_addr_list):
        for ip in ip_addr_list:
            test_file = '/tmp' + '/' + ip + '.txt'
            os.remove(test_file)

    def add_avaiable_device_and_ip_list(self):
        a = Network_speed_test_examine()
        for device in device_list:
            device_ipaddr = a.device_ipaddr_check(device).replace('/24\n', '')
            if device_ipaddr and device != 'lo':
                local_device_list.append(device)
                local_ip_list.append(device_ipaddr)
            else:
                pass

    def iperf_host_list(self):
        if len(test_cluster_host) >= 4:
            test_iperf_server_list = []
            local_device_ipaddr = manager_ip_address
            list = local_device_ipaddr.split('.', 4)
            if list[3] in test_cluster_host:
                index_position = test_cluster_host.index(list[3])
                test_iperf_server_list = \
                    [test_cluster_host[(i + index_position + 1) % len(test_cluster_host)] for i in xrange(3)]
        return test_iperf_server_list


    def iperf_host_cluster(self):
        instance = Network_speed_test_examine()
        iperf_client_cluster_list = []
        for host in instance.iperf_host_list():
            for local_ip in local_ip_list:
                list = local_ip.split('.', 4)
                list[3] = host
                target_iperf_server_ip = '.'.join(list)
                iperf_client_cluster_list.append(target_iperf_server_ip)
        return iperf_client_cluster_list

if __name__ == '__main__':
    a = Network_speed_test_examine()
    a.add_avaiable_device_and_ip_list()
    firewalld_state_bool = a.firewalld_service_stop()
    for local_ip in local_ip_list:
        a.device_iperf_server_check(local_ip)

    time.sleep(2)

    for iperf_server_ip in a.iperf_host_cluster():
        t = threading.Thread(target=a.device_iperf_clinet_check, args=(iperf_server_ip, check_time+10))
        t.start()
        time.sleep(1)
    t.join()

    time.sleep(10)

    for device in local_device_list:
        t = threading.Thread(target=a.network_device_receive_flow_check, args=(device, check_time))
        t.start()
        time.sleep(1)
    t.join()

    time.sleep(2)

    a.kill_iperf_server()
    if int(firewalld_state_bool) == 0:
        a.firewalld_service_start()
    else:
        pass
    a.test_file_delete(local_ip_list)
