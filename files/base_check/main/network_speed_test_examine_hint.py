# -*- coding: utf-8 -*-
import sys
sys.path.append("/tmp/base_check/")
import pdb
from network_check.network_speed_test_examine import *

if __name__ == '__main__':
    a = Network_speed_test_examine()
    a.add_avaiable_device_and_ip_list()
    firewalld_state_bool = a.firewalld_service_stop()
    for local_ip in local_ip_list:
        a.device_iperf_server_check(local_ip)
     
    time.sleep(2)     

    for iperf_server_ip in a.iperf_host_cluster():
        t = threading.Thread(target=a.device_iperf_clinet_check, args=(iperf_server_ip, check_time + 30))
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
