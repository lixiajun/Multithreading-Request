#coding=utf-8
#author:xjli@d-ear.com
from train_verify import one_person_train,one_person_verify
import time,os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
def train_action(url,train_path):             #进行所有人的预留操作，比如传入预留路径‘confused/train’
    start_time = time.time()
    cust_id_list = os.listdir(train_path)
    failure_num, success_num = 0, 0
    for cust_id in cust_id_list:
        train_voice_path = train_path + '/' + cust_id
        result = one_person_train(url=url, cust_id=cust_id, train_voice_path=train_voice_path)
        if result == "successful":
            success_num += 1                             #统计成功的个数
        else:
            failure_num += 1
    end_time = time.time()
    print("Trains complete, success[%d], fail[%d]. test cost %d s" % (success_num, failure_num, end_time - start_time))

def verify_action(url,verify_path):            #进行所有人的验证操作，比如传入验证语音路径 ‘confused/verify’，传入train的路径是为了统计speaker_id的列表
    start_time = time.time()
    with open('vpr_test_list') as vpr_file:
        vpr_file_list = vpr_file.readlines()    # 类似： ['1000\t1_1000_female_20170801103222_09586172_iPhone9,2-iOS10.3_verify_4.wav\n', '1000\t1_1000_female_20170801103212_75142689_iPhone9,2-iOS10.3_verify_2.wav\n']
    cust_id_list,file_name_list = [],[]
    failure_num, success_num = 0, 0
    failure_information_list = []
    vpr_result_dict = {}
    for items in vpr_file_list:                     # i 类似：‘1000\t1_1000_female_20170801103222_09586172_iPhone9,2-iOS10.3_verify_4.wav\n’
        cust_id_list.append(items.split('\t')[0])
        file_name_list.append(items.split('\t')[1].replace('\n',''))
    for num in xrange(len(cust_id_list)):
        cust_id = cust_id_list[num]
        voice_name = file_name_list[num]
        result = one_person_verify(url,cust_id,verify_path,voice_name)
        if result[0] != "failure":
            success_num += 1
            vpr_result_dict[result[1]] = result[2]
            print("cust_id : %s ,voice_name : %s , score is %s " % (cust_id,voice_name,result[0]))
        else:
            failure_num += 1
            error_infomation = "cust_id : %s ,voice_name : %s faild , failure reason is %s" % (cust_id, voice_name, result[1])
            failure_information_list.append(error_infomation)

    end_time = time.time()
    print("=======   Trains complete, success[%d], fail[%d]. test cost %ds   =======" % (success_num, failure_num, end_time - start_time))
    print("failure list is:")
    for error_info in failure_information_list:
        print(error_info)
    with open("vpr_result",'w') as fi:
        for i in vpr_file_list:
            fi.write('%s \t %.2f \n' % (i.replace('\n',''),float(vpr_result_dict[i.replace('\n','')])))


if  __name__ == "__main__":
    train_url = "http://10.0.2.159:8101/voiceprint/training"
    train_path = "./confused/train"
    train_action(url=train_url,train_path=train_path)
    #verify_path = "./confused/verify"
    #verify_url = "http://10.0.2.159:8101/voiceprint/verification"
    #verify_action(url=verify_url,verify_path=verify_path)