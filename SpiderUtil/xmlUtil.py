import sys

sys.path.append('../')

import xml.etree.ElementTree as ET
from Config import xml_config

from LOL.lolMongoClient import get_all_hero, save_xml_to_mongo
from GOK.gokMongoClient import gok_get_all_hero


def only_one_run():
    list_tmp = gok_get_all_hero()
    list_tmp_dr = []

    root_data = ET.Element("data")  # 创建根节点
    for item in list_tmp:
        if item.get('heroname') not in list_tmp_dr:
            list_tmp_dr.append(item.get('heroname'))

            hero_element = ET.SubElement(root_data, "hero")  # 创建子节点，并添加属性
            hero_element.attrib = {"name": item.get('heroname')}

            hero_element_name = ET.SubElement(hero_element, "another_name")  # 创建子子节点，并添加数据
            hero_element_name.text = item.get('heroname')
            hero_element_name = ET.SubElement(hero_element, "another_name")  # 创建子子节点，并添加数据
            hero_element_name.text = "别名"

            tree = ET.ElementTree(root_data)  # 创建elementtree对象，写文件
            tree.write(xml_config['GOK_XML_FILE_PATH'], encoding="UTF-8")
            """
            2019-06-14 缺少巨魔
            """


def read_Xml():
    tree = ET.parse(xml_config['XML_FILE_PATH'])
    root = tree.getroot()
    for hero in root.iter('hero'):
        dict = {'name': hero.attrib['name']}
        i = 0
        for another_name in hero.iter('another_name'):
            i += 1
            dict.update({'another' + str(i): another_name.text.strip()})
        save_xml_to_mongo(dict)


if __name__ == '__main__':
    # read_Xml()  # 读取并保存到Mongo
    # print('NULL')
    #only_one_run()
    pass
