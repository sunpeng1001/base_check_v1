# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("/tmp/base_check/")

class System_examine():

    def tcp_and_udp_port_check(self):
        listen_tcp_port_num = os.popen("ss -lantu4|grep LISTEN|grep -w tcp "
                                       "|awk '{print $5}'|awk -F ':' '{print $2}'|uniq|wc -l").read()
        listen_tcp_port = os.popen("ss -lantu4|grep LISTEN|grep -w tcp "
                                   "|awk '{print $5}'|awk -F ':' '{print $2}'|uniq|tr '\n' ' '").read()
        listen_udp_port_num = os.popen("ss -lantu4|grep udp|awk '{print $5}'|awk -F ':' '{print $2}'|uniq|wc -l").read()
        listen_udp_port = os.popen("ss -lantu4|grep udp|awk '{print $5}'|awk -F ':' '{print $2}'|uniq|tr '\n' ' '").read()
        return ('TCP_Port_Num:%d  TCP_Port:%s  UDP_Port_Num:%d  UDP_Port:%s'
              %(int(listen_tcp_port_num),listen_tcp_port,int(listen_udp_port_num),listen_udp_port ))

if __name__ == "__main__":
    a = System_examine()
    print a.tcp_and_udp_port_check()