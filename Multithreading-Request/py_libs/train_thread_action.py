#coding=utf-8
#author:xjli@d-ear.com
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

class TrainThread(threading.Thread):
    def __init__(self,url,train_path,cust_id_list):
        super(TrainThread, self).__init__()  # 调用父类的构造函数
        self.url = url
        self.train_path = train_path
        self.cust_id_list = cust_id_list
    def run(self):
        global success_num,failure_num
        for num in xrange(len(self.cust_id_list)):
            cust_id = self.cust_id_list[num]
            train_voice_path = self.train_path + '/' + cust_id
            result = one_person_train(self.url, cust_id, train_voice_path)
            if mutex.acquire():
                if result[0] == "successful":
                    success_num += 1  # 统计成功的个数
                    print('%s train successfully' % cust_id)
                else:
                    failure_num += 1
                    print("%s train faild,infomation is %s" % (cust_id, result[1]))
                mutex.release()

def train_thread_action(train_path,train_url,thread_num=1):
    start_time = time.time()
    cust_id_list = os.listdir(train_path)
    global success_num, failure_num
    success_num,failure_num = 0,0
    threads_list = []
    all_task_numbers = len(cust_id_list)
    if int(thread_num) > int(all_task_numbers):
        thread_num = all_task_numbers
        print("your thread_num is over all_task_numbers,so choose the all_task_numers as thread_num")
    one_thread_tasks, last_thread_tasks = calculate_thread_task(all_task_numbers=all_task_numbers,
                                                                thread_num=thread_num)
    for i in xrange(1, thread_num + 1):
        if i < thread_num:
            thread_cust_id_list = cust_id_list[(i - 1) * one_thread_tasks: i * one_thread_tasks]
        else:
            thread_cust_id_list = cust_id_list[-last_thread_tasks:]
        thread = TrainThread(url=train_url, train_path=train_path, cust_id_list=thread_cust_id_list)
        threads_list.append(thread)
    print(threads_list)
    for thread in threads_list:
        thread.start()
    for thread in threads_list:
        thread.join()

    end_time = time.time()
    print("=======   train complete, success[%d], fail[%d]. test cost %ds   =======" % (
        success_num, failure_num, end_time - start_time))

if __name__ == "__main__":
    train_url = "http://10.0.2.159:8101/voiceprint/training"
    train_path = "../confused/train"
    train_thread_action(train_path,train_url,thread_num=2)