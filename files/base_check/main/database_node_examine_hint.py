# -*- coding: utf-8 -*-
import sys
sys.path.append("/tmp/base_check/")
from database_node_check.database_node_examine import *

if __name__ == '__main__':
    instance = Database_node_examine()
    print instance.numa_state_check()
    print instance.default_limit_file_num_check()
    print instance.default_limit_proc_num_check()
    for i in instance.data_disk_check():
        print i
