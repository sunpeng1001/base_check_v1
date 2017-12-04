# -*- coding: utf-8 -*-
import os

#common var
manager_ip_address = '{{ inventory_hostname }}'

#network_base_check module var
target_net_device = '{{ target_net_device }}'
target_net_device_mtu = {{ target_net_device_mtu }}
target_net_device_speed = {{ target_net_device_speed }}
target_net_gateway = '{{ target_net_getway }}'

#network_connection_check moduler var
target_devices = {{ target_devices }}
ping_test_duration = '{{ ping_test_duration }}'
ping_test_timeout = {{ ping_test_timeout }}

#network_device_mac_check moduler var
mac_check_data_file = '{{ mac_check_data_file }}'

#network device press test var
test_cluster_manger_network = '{{ test_cluster_manger_network }}'
test_cluster_host = {{ test_cluster_host }}
check_time = {{ check_time }}

#database_node_check module var
default_limit_file_conf = {{ defaultlimitnofile_num }}
default_limit_proc_conf = {{ defaultlimitnproc_num }}
database_conf_disk = '{{ database_dir }}'
databse_disk_conf_volume = '{{ database_dir_capacity }}'

#cpu_check moduler var
cpu_check_data_file = '{{ cpu_check_data_file }}'
cpu_vendor_conf = '{{ cpu_vendor_conf }}'
cpu_socket_num_conf = {{ cpu_socket_num_conf }}
cpu_cores_per_socket_conf = {{ cpu_cores_per_socket_conf }}
cpu_threads_per_core_conf = {{ cpu_threads_per_core_conf }}
