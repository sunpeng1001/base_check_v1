# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("/tmp/base_check/")
from conf.base_conf import default_limit_file_conf
from conf.base_conf import default_limit_proc_conf
from conf.base_conf import database_conf_disk
from conf.base_conf import databse_disk_conf_volume


class Database_node_examine():
    def numa_state_check(self):
        numa_state = os.popen("cat /etc/grub2.cfg |grep numa=off &>/dev/null;echo $?").read()
        if int(numa_state) == 0:
            return ('Numa_State:OFF')
        else:
            return ('Numa_State:ON')

    def  default_limit_file_num_check(self):
        default_limit_file_num = os.popen("cat /etc/systemd/system.conf"
                                          "|grep ^DefaultLimitNOFILE|awk -F '=' '{print $2}'").read()

        if default_limit_file_num.strip() != '':
            if int(default_limit_file_num) == default_limit_file_conf:
                # when it print Error,means it's value is not right
                # when it print None,means it's value is not defined
                return ('DefaultLimitNOFILE:%s' %int(default_limit_file_num))
            else:
                return ('DefaultLimitNOFILE:Error')
        else:
              return ('DefaultLimitNOFILE:None')

    def default_limit_proc_num_check(self):
        default_limit_proc_num = os.popen("cat /etc/systemd/system.conf"
                                          "|grep ^DefaultLimitNPROC|awk -F '=' '{print $2}'").read()
        if default_limit_proc_num.strip() != '':
            if int(default_limit_proc_num) == default_limit_proc_conf:
                return ('DefaultLimitNPROC:%s' %int(default_limit_proc_num))
            else:
                return ('DefaultLimitNPROC:Error')
        else:
            return ('DefaultLimitNPROC:None')

    def data_disk_check(self):
        os.environ['target_block'] = database_conf_disk
        database_data_dir = os.popen("lsblk|grep ^$target_block|awk '{print $1}'").read()
        database_data_disk_volume = os.popen("lsblk|grep ^$target_block|awk '{print $4}'").read()
        if database_conf_disk == database_data_dir.strip():
            data_disk = ('Data_disk:%s' % database_conf_disk)
            if databse_disk_conf_volume == database_data_disk_volume.strip():
                data_disk_volume = ('Data_disk_volume:%s'%databse_disk_conf_volume)
            else:
                data_disk_volume = ('Data_disk_volume:Error')
        else:
            data_disk = ('Data_disk:None')
            data_disk_volume = ('Data_disk_volume:None')
        return data_disk,data_disk_volume

if __name__ == "__main__":
    a = Database_node_examine()
    print a.numa_state_check()
    print a.default_limit_file_num_check()
    print a.default_limit_proc_num_check()
    print a.data_disk_check()