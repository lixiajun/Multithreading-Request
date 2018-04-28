#coding=utf-8
#author:lxj
import requests,urllib2
from deal_xml import deal_xml


def get_train_txt(url,cust_id):
    """获取预留文本"""
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
             <OPERATION_TYPE>1</OPERATION_TYPE>            
             <CUST_ID>%s</CUST_ID>            
             <DEVICE_INFO></DEVICE_INFO>            
             <TYPE>4097</TYPE>    
             </ENTITY>  
             </TX_BODY>
             <TX_EMB> 
             </TX_EMB>
             </TX>  
             """ % cust_id
    headers = {
        'content-type': "text/xml",
        'cache-control': "no-cache",
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    response_xml_content = response.text            #获取到返回的xml文件内容
    #print(response.text)
    return_code_and_info = deal_xml(response_xml_content, *["RETURN_CODE", "RETURN_INFO"])

    if return_code_and_info["RETURN_CODE"] == "0":
        return_data_dict = deal_xml(response_xml_content,*['TRAINING_ID','TEXT'])
        training_id, number_text = return_data_dict['TRAINING_ID'],return_data_dict['TEXT']   # TRAINING_ID标签对之间的数据
        number_text_list = [i.split(":")[1] for i in number_text.split(',')]
        #print("training_id is %s , number_text is %s" % (training_id,number_text_list))
        return (training_id, number_text_list)
    else:
        print(u'get train_text fail,error code is:%s , error_info is %s' % (return_code_and_info["RETURN_CODE"], return_code_and_info["RETURN_INFO"]))

def get_verify_txt(url,cust_id):
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
                     <OPERATION_TYPE>1</OPERATION_TYPE>
                     <CUST_ID>%s</CUST_ID>
                     <DEVICE_INFO></DEVICE_INFO>
                     <TYPE>8193</TYPE>    
                 </ENTITY>  
                 </TX_BODY>
                 <TX_EMB> 
                 </TX_EMB>
                 </TX>  
                 """ % cust_id
    headers = {
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    response_xml_content = response.text
    #print(response.text)
    return_code_and_info = deal_xml(response_xml_content,*["RETURN_CODE","RETURN_INFO"])

    if return_code_and_info["RETURN_CODE"] == "0":
        return_verifyid_and_text = deal_xml(response_xml_content, *[ "VERIFICATION_ID", "TEXT"])
        #print(return_verifyid_and_text["VERIFICATION_ID"],return_verifyid_and_text["TEXT"])
        return (return_verifyid_and_text["VERIFICATION_ID"],return_verifyid_and_text["TEXT"])
    else:
        print(u'get verify_text fail,error code is:%s,error_info is %s' % (return_code_and_info["RETURN_CODE"],return_code_and_info["RETURN_INFO"]))


if __name__ == "__main__":
    url = "http://10.0.2.159:8101/voiceprint/training"
    cust_id = "00002"
    get_train_txt(url, cust_id)
    #url = "http://10.0.2.159:8101/voiceprint/verification"
    #get_verify_txt(url=url,cust_id=cust_id)
