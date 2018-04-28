#coding=utf-8
#author:lxj
import requests,base64
from deal_xml import deal_xml
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def get_voice_content(voice_path):
    """打开语音文件，获取文件内容。使用encodestring方法，以二进制的方式打开文件"""
    with open(voice_path,'rb') as fi:
        voice_content = fi.read()
        voice_base64 = base64.encodestring(voice_content)
    return voice_base64


def upload_train_voice(url,train_id,num_order,num_text,voice_path):
    """train_id是session_id，num_text是8位数字窜，num_order是数字窜索引，voice_path是base64处理后的语音文件
    预留一共要5次上传语音，本方法只进行一次上传语音，所以5次之后才能知道是否预留成功。所以会把RETURN_CODE返回，
    供调用者统计，来确认是否预留成功"""
    voice_base64 = get_voice_content(voice_path)
    payload = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
             <TX>
             <TX_HEADER>    
             <SYS_HDR_LEN>100</SYS_HDR_LEN>
             <SYS_PKG_VRSN>01</SYS_PKG_VRSN>    
             <SYS_TTL_LEN>400</SYS_TTL_LEN>    
             <SYS_REQ_SEC_ID>0123456789</SYS_REQ_SEC_ID>   
             <SYS_SND_SEC_ID>9876543210</SYS_SND_SEC_ID>    
             <SYS_TX_CODE>VoiceServices</SYS_TX_CODE>    
             <SYS_TX_VRSN>01</SYS_TX_VRSN>   
             <SYS_TX_TYPE>00000</SYS_TX_TYPE>    
             <SYS_RESERVED>AA</SYS_RESERVED>    
             <SYS_EVT_TRACE_ID>yyyyMMddHHmmssms</SYS_EVT_TRACE_ID>    
             <SYS_SND_SERIAL_NO>0000000023</SYS_SND_SERIAL_NO>    
             <SYS_PKG_TYPE>1</SYS_PKG_TYPE>    
             <SYS_MSG_LEN>100</SYS_MSG_LEN>    
             <SYS_IS_ENCRYPTED>0</SYS_IS_ENCRYPTED>    
             <SYS_ENCRYPT_TYPE>3</SYS_ENCRYPT_TYPE>    
             <SYS_COMPRESS_TYPE>0</SYS_COMPRESS_TYPE>    
             <SYS_EMB_MSG_LEN>0</SYS_EMB_MSG_LEN>    
             <SYS_REQ_TIME>yyyyMMddHHmmssms</SYS_REQ_TIME>    
             <SYS_TIME_LEFT>HHmmssms</SYS_TIME_LEFT>    
             <SYS_PKG_STS_TYPE>00</SYS_PKG_STS_TYPE>  
             </TX_HEADER>  
             <TX_BODY>    
             <COMMON>      
             <COM1>        
             <TXN_INSID>440000000</TXN_INSID>        
             <TXN_ITT_CHNL_ID>0130</TXN_ITT_CHNL_ID>        
             <TXN_ITT_CHNL_CGY_CODE>0001</TXN_ITT_CHNL_CGY_CODE>       
             <TXN_DT>yyyyMMdd</TXN_DT>        
             <TXN_TM>HHmmss</TXN_TM>        
             <TXN_STFF_ID>999999</TXN_STFF_ID>        
             <MULTI_TENANCY_ID>CN000</MULTI_TENANCY_ID>        
             <LNG_ID>zh-cn</LNG_ID>      
             </COM1>    
             </COMMON>    
             <ENTITY>
			 <OPERATION_TYPE>2</OPERATION_TYPE>
             <TRAINING_ID>%s</TRAINING_ID>
             <TEXT>%s</TEXT>
             <INDEX>%s</INDEX>
             <VOICE>%s</VOICE>
             <VOICE_LENGTH>1</VOICE_LENGTH>
		     </ENTITY>
             </TX_BODY>
             <TX_EMB> 
             </TX_EMB>
             </TX>  
             """ % (train_id,num_text,num_order,voice_base64)
    headers = {
        'content-type': "text/xml",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return_code_info = deal_xml(response.text,*["RETURN_CODE","RETURN_INFO"])
    return (return_code_info["RETURN_CODE"],return_code_info["RETURN_INFO"])

def upload_verify_voice(url,verify_id,voice_path):
    """ 上传验证语音，与train不同，1个人1次验证操作的话，只会上传1次语音。所以一次上传语音就能确定一次验证是否成功。
    train_id是session_id，num_text是8位数字窜，num_order是数字窜索引，voice_path是语音文件的路径
    该方法进行一次验证的上传语音
    这里不像train用元组返回，而是采用字典的原因：是否验证成功和失败，所需返回的元素是不一样的.
    验证成功和失败，标准是，语音上传是否成功，而非分数是否通过"""
    voice_base64 = get_voice_content(voice_path)
    payload = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
                 <TX>
                 <TX_HEADER>    
                 <SYS_HDR_LEN>100</SYS_HDR_LEN>
                 <SYS_PKG_VRSN>01</SYS_PKG_VRSN>    
                 <SYS_TTL_LEN>400</SYS_TTL_LEN>    
                 <SYS_REQ_SEC_ID>0123456789</SYS_REQ_SEC_ID>   
                 <SYS_SND_SEC_ID>9876543210</SYS_SND_SEC_ID>    
                 <SYS_TX_CODE>VoiceServices</SYS_TX_CODE>    
                 <SYS_TX_VRSN>01</SYS_TX_VRSN>   
                 <SYS_TX_TYPE>00000</SYS_TX_TYPE>    
                 <SYS_RESERVED>AA</SYS_RESERVED>    
                 <SYS_EVT_TRACE_ID>yyyyMMddHHmmssms</SYS_EVT_TRACE_ID>    
                 <SYS_SND_SERIAL_NO>0000000023</SYS_SND_SERIAL_NO>    
                 <SYS_PKG_TYPE>1</SYS_PKG_TYPE>    
                 <SYS_MSG_LEN>100</SYS_MSG_LEN>    
                 <SYS_IS_ENCRYPTED>0</SYS_IS_ENCRYPTED>    
                 <SYS_ENCRYPT_TYPE>3</SYS_ENCRYPT_TYPE>    
                 <SYS_COMPRESS_TYPE>0</SYS_COMPRESS_TYPE>    
                 <SYS_EMB_MSG_LEN>0</SYS_EMB_MSG_LEN>    
                 <SYS_REQ_TIME>yyyyMMddHHmmssms</SYS_REQ_TIME>    
                 <SYS_TIME_LEFT>HHmmssms</SYS_TIME_LEFT>    
                 <SYS_PKG_STS_TYPE>00</SYS_PKG_STS_TYPE>  
                 </TX_HEADER>  
                 <TX_BODY>    
                 <COMMON>      
                 <COM1>        
                 <TXN_INSID>440000000</TXN_INSID>        
                 <TXN_ITT_CHNL_ID>0130</TXN_ITT_CHNL_ID>        
                 <TXN_ITT_CHNL_CGY_CODE>0001</TXN_ITT_CHNL_CGY_CODE>       
                 <TXN_DT>yyyyMMdd</TXN_DT>        
                 <TXN_TM>HHmmss</TXN_TM>        
                 <TXN_STFF_ID>999999</TXN_STFF_ID>        
                 <MULTI_TENANCY_ID>CN000</MULTI_TENANCY_ID>        
                 <LNG_ID>zh-cn</LNG_ID>      
                 </COM1>    
                 </COMMON>    
                 <ENTITY>
    			 <OPERATION_TYPE>2</OPERATION_TYPE>
                 <VERIFICATION_ID>%s</VERIFICATION_ID>
                 <VOICE>%s</VOICE>
                 <VOICE_LENGTH>1</VOICE_LENGTH>
    		     </ENTITY>
                 </TX_BODY>
                 <TX_EMB> 
                 </TX_EMB>
                 </TX>  
                 """ % (verify_id,voice_base64)
    headers = {
        'content-type': "text/xml",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return_code_info = deal_xml(response.text, *["RETURN_CODE", "RETURN_INFO"])
    if return_code_info["RETURN_CODE"] == "0":
        return {"RETURN_CODE":return_code_info["RETURN_CODE"],"SCORE":deal_xml(response.text, *["SCORE"])["SCORE"]}
    else:
        return {"RETURN_CODE":return_code_info["RETURN_CODE"],"RETURN_INFO":return_code_info["RETURN_INFO"]}

if __name__ == "__main__":
    #url = "http://10.0.2.159:8101/voiceprint/training"
    #train_id = "92ca5106214a43d78056b88fd1ff4e8c"
    #upload_train_voice(url,train_id,'1','20799053','./confused/train/yk0197/2ec86ee63ac548aa8b930a7fd690c636')
    url = "http://10.0.2.159:8101/voiceprint/verification"
    verify_id = "0a7e2292711541df8cd21116e7c3cb1f"
    upload_verify_voice(url,verify_id,'./confused/verify/eightworlds_11101033228141_male_20171110103534_0_Xiaomiphone-Android_train_8.wav')

