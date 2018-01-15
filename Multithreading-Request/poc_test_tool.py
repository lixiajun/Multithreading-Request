#!/usr/bin/python
#coding=utf-8
#author:xjli@d-ear.com
import sys,os
sys.path.append('./py_libs/requests_libs')
from poc_conf import ip,port
from py_libs.train_thread_action import train_thread_action
from py_libs.verify_thread_action import verify_thread_action

def dire_exist(*dire_path):
    for dire in dire_path:
        if not os.path.exists(dire):
            print("cant find the %s" % i)
            sys.exit()
def file_exist(file_path):
    if not os.path.isfile(file_path):
        print("cant find the %s" % i)
        sys.exit()

def act(ip,port):
    if len(sys.argv) !=5 and len(sys.argv) !=6:
        print("The correct parameters should been [train/verify]  [train_voice path]  [verify_voice path] [vpr_test_list] [thread_num],please input correct parameters again ")
        sys.exit()
    dire_exist(*[sys.argv[2], sys.argv[3]])
    file_exist(sys.argv[4])
    train_path = sys.argv[2]
    verify_path = sys.argv[3]
    vpr_test_list_file_path = './' + sys.argv[4]
    if len(sys.argv) == 5:
        thread_num = 1
    else:
        thread_num = int(sys.argv[5])
    if sys.argv[1] == "train":
        train_url = "http://%s:%s/voiceprint/training" % (ip,port)
        train_thread_action(train_path,train_url,thread_num)
    elif sys.argv[1] == "verify":
        verify_url = "http://%s:%s/voiceprint/verification" % (ip,port)
        print(verify_path)
        verify_thread_action(verify_path,verify_url,vpr_test_list_file_path,thread_num)
    else:
        print("The correct parameters should been [train/verify]  [train_voice path]  [verify_voice path] [vpr_test_list] [thread_num],please input correct parameters again")
        sys.exit()
if __name__ == "__main__":
    act(ip,port)
