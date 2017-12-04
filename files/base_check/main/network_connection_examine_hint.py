# -*- coding: utf-8 -*-
import sys
sys.path.append("/tmp/base_check/")
from network_check.network_connection_examine import *

if __name__ == '__main__':
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