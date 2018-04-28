#coding=utf-8
#author:lxj
from train_verify import one_person_train,one_person_verify
import time,os,threading
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


mutex = threading.Lock()
def calculate_thread_task(all_task_numbers,thread_num=1):
    one_thread_tasks = int(all_task_numbers) / int(thread_num)
    last_thread_tasks = (int(all_task_numbers) % int(thread_num)) + one_thread_tasks
    return [one_thread_tasks,last_thread_tasks]


class VerifyThread(threading.Thread):
    def __init__(self,url,verify_path,cust_id_list,file_name_list):
        super(VerifyThread, self).__init__()  # 调用父类的构造函数
        self.url = url
        self.verify_path = verify_path
        self.cust_id_list = cust_id_list
        self.file_name_list = file_name_list
    def run(self):
        global success_num,failure_num,failure_information_list,vpr_result_dict
        for num in xrange(len(self.cust_id_list)):
            cust_id = self.cust_id_list[num]
            voice_name = self.file_name_list[num]
            result = one_person_verify(self.url, cust_id, self.verify_path,voice_name)
            if mutex.acquire():
                if result[0] != "failure":
                    success_num += 1
                    vpr_result_dict[result[1]] = result[2]         #result[1]和result[2]分别就是vpr_result结果文件的第一，二列，和第三列。
                    print("cust_id : %s ,voice_name : %s , score is %s " % (cust_id, voice_name, result[0]))
                else:
                    failure_num += 1
                    error_infomation = "cust_id : %s ,voice_name : %s faild , failure reason is %s" % (
                    cust_id, voice_name, result[1])
                    failure_information_list.append(error_infomation)
                mutex.release()
def verify_thread_action(verify_path,verify_url,verify_list_file_name,thread_num=1):
    start_time = time.time()
    with open(verify_list_file_name) as vpr_file:
        vpr_file_list = vpr_file.readlines()  # 类似： ['1000\t1_1000_female_20170801103222_09586172_iPhone9,2-iOS10.3_verify_4.wav\n', '1000\t1_1000_female_20170801103212_75142689_iPhone9,2-iOS10.3_verify_2.wav\n']
    cust_id_list, file_name_list = [], []
    for i in vpr_file_list:  # i 类似：‘1000\t1_1000_female_20170801103222_09586172_iPhone9,2-iOS10.3_verify_4.wav\n’
        cust_id_list.append(i.split('\t')[0])
        file_name_list.append(i.split('\t')[1].replace('\n', ''))
    global success_num, failure_num, failure_information_list, vpr_result_dict
    success_num, failure_num, failure_information_list, vpr_result_dict = 0, 0, [], {}
    threads_list = []
    all_task_numbers = len(vpr_file_list)
    one_thread_tasks, last_thread_tasks = calculate_thread_task(all_task_numbers=all_task_numbers,
                                                                thread_num=thread_num)

    for i in xrange(1, thread_num + 1):
        if i < thread_num:
            thread_cust_id_list = cust_id_list[(i - 1) * one_thread_tasks: i * one_thread_tasks]
            thread_file_name_list = file_name_list[(i - 1) * one_thread_tasks: i * one_thread_tasks]
        else:
            thread_cust_id_list = cust_id_list[-last_thread_tasks:]
            thread_file_name_list = file_name_list[-last_thread_tasks:]
        thread = VerifyThread(url=verify_url, verify_path=verify_path, cust_id_list=thread_cust_id_list,
                          file_name_list=thread_file_name_list)
        threads_list.append(thread)
    print(threads_list)
    for thread in threads_list:
        thread.start()
    for thread in threads_list:
        thread.join()

    end_time = time.time()
    print("=======   verify complete, success[%d], fail[%d]. test cost %ds   =======" % (
        success_num, failure_num, end_time - start_time))
    print("failure list is:")
    for error_info in failure_information_list:
        print(error_info)
    with open("./Result/vpr_result_online.txt", 'wb') as fi:
        for i in vpr_file_list:
            fi.write('%s\t %.2f \n' % (i.replace('\n', ''), float(vpr_result_dict[i.replace('\n', '')])))

if __name__ == "__main__":
    verify_path = "../confused/verify"
    verify_url = "http://10.0.2.159:8101/voiceprint/verification"
    verify_list_file_name = "../vpr_test_list"
    verify_thread_action(verify_path,verify_url,verify_list_file_name,thread_num=25)
