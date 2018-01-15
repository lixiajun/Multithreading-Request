#coding=utf-8
#author:xjli@d-ear.com
from get_num_txt import get_train_txt,get_verify_txt
from upload_voice import upload_train_voice,upload_verify_voice
import os,time

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


def one_person_train(url,cust_id,train_voice_path):       #进行一个人的预留，包括获取文本和5次上传语音
    try:
        train_id , number_text_list = get_train_txt(url=url,cust_id=cust_id)
    except:
        print('Can\'t connect the smb service,please check the ip and port ')
        sys.exit()
    voice_file_list = [ train_voice_path + '/' + i for i in os.listdir(train_voice_path) ]
    return_code_0_list = []
    error_info_list = []
    for num_order in range(1,6):
        return_code,return_info= upload_train_voice(url=url,
                           train_id=train_id,num_order=str(num_order),
                           num_text=number_text_list[num_order - 1],
                           voice_path=voice_file_list[num_order - 1])
        if return_code != "0":
            error_info_list.append(return_info)
        else:
            return_code_0_list.append(return_code)
    if len(return_code_0_list) == 5:
        #print('%s train successfully' % cust_id)
        return ["successful"]                                       #确定1次预留是否成功
    else:
        #print("%s train faild,infomation is %s" % (cust_id,error_info_list[0]))
        return ["failed",error_info_list[0]]

def one_person_verify(url,cust_id,verify_path,voice_name):     #进行一个人的一次验证，包括获取文本和上传语音
    verify_id , _ = get_verify_txt(url,cust_id)
    verify_voice_path = os.path.join(verify_path, voice_name)
    result_dict = upload_verify_voice(url=url, verify_id=verify_id, voice_path=verify_voice_path)
    if "SCORE" in result_dict.keys():
        vpr_result_key = cust_id + '\t' + voice_name
        vpr_result_value = result_dict["SCORE"]
        #print("cust_id : %s ,voice_name : %s , score is %s " % (cust_id, voice_name, result_dict["SCORE"]))
        return [result_dict["SCORE"], vpr_result_key, vpr_result_value]
    else:
        return ["failure", result_dict["RETURN_INFO"]]




if  __name__ == "__main__":
    url = "http://10.0.2.159:8101/voiceprint/training"
    cust_id = "1111"
    train_voice_path = './confused/train/yk_noheader'
    one_person_train(url, cust_id, train_voice_path)

    verify_path = "./confused/verify/"
    verify_url = "http://10.0.2.159:8101/voiceprint/verification"
    one_person_verify
