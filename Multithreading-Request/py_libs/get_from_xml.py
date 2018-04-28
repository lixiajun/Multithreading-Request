#coding=utf-8
#author:lxj
import xml.dom.minidom

#打开xml文档
xml_open = xml.dom.minidom.parse('1.xml')   #打开xml文档
#xml_open = xml.dom.minidom.parseString(response_xml_string)  # 传入存有xml的字符串
xml_elements_objects = xml_open.documentElement          #得到文档元素对象
TRAINING_ID_xml_list = xml_elements_objects.getElementsByTagName('TRAINING_ID')   #得到标签名是TRAINING_ID的对象的列表
TRAINING_ID = TRAINING_ID_xml_list[0].firstChild.data  #列表第一个元素是TRAINING_ID标签，取标签对之间的数据

number_text_xml_list = xml_elements_objects.getElementsByTagName('TEXT')
number_text = number_text_xml_list[0].firstChild.data
number_text_list = [ i.split(":")[1] for i in number_text.split(',') ]
print(TRAINING_ID,number_text_list)   #TRAINING_ID标签对之间的数据

