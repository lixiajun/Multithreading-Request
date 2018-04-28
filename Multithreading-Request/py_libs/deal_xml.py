#coding=utf-8
#author:lxj
import xml.dom.minidom
def deal_xml(xml_content,*element):       #传入字符窜格式的xml，以及想要获得数据的对应的标签
    xml_open = xml.dom.minidom.parseString(xml_content)  # 传入存有xml的字符串
    xml_elements_objects = xml_open.documentElement  # 得到文档元素对象
    return_data_dict = {}
    for elem in element:
        TRAINING_ID_xml_list = xml_elements_objects.getElementsByTagName(elem)  # 得到标签名是element的对象的列表
        elem_data = TRAINING_ID_xml_list[0].firstChild.data  # 列表第一个元素是element标签，取标签对之间的数据
        return_data_dict[elem] = elem_data
    return return_data_dict                   #返回标签之间的数据

if __name__ == "__main__":
    string = open('1.xml').read()
    elem_list = ["RETURN_CODE","RETURN_INFO","TRAINING_ID","TEXT"]
    dict = deal_xml(string,*elem_list)
    print(dict)
