import pymongo
import datetime
import sys

sys.path.append('../')

from Config import mongo_config

client = pymongo.MongoClient(mongo_config['MONGO_URL'])
db = client[mongo_config['MONGO_DB']]

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

"""
爬取保存到MongoDB
"""


def save_to_mongo(hero):
    if db[mongo_config['MONGO_TABLE']].insert(hero.convert_to_dict()):
        print('存储成功！', str(hero.convert_to_dict()))
        client.close()
        return True
    client.close()
    print('存储失败')
    return False


"""
根据英雄名称，返回信息
"""


def get_hero(hero_name):
    search_set = db[mongo_config['MONGO_TABLE']]
    list_tmp = []
    for x in search_set.find({'cn_name': hero_name, 'day':yesterday.strftime('%Y-%m-%d')}):
        list_tmp.append(x)
    client.close()
    if len(list_tmp) > 0:
        return list_tmp
    else:
        return None


"""
获取所有英雄
"""


def get_all_hero():
    search_set = db[mongo_config['ANOTHER_NAME_TABLE']]
    list_tmp = []
    for x in search_set.find():
        list_tmp.append(x)
    client.close()
    if len(list_tmp) > 0:
        return list_tmp
    else:
        return None


"""
保存xml到MongoDB
"""


def save_xml_to_mongo(hero_another):
    if db[mongo_config['ANOTHER_NAME_TABLE']].insert(hero_another):
        print('存储成功！', str(hero_another))
        client.close()
        return True
    client.close()
    print('存储失败')
    return False


"""
根据英雄别名，返回信息
"""


def get_hero_name_by_another(hero_another_name):
    search_set = db[mongo_config['ANOTHER_NAME_TABLE']]
    list_tmp = []
    for x in search_set.find({"$or": [{"name": hero_another_name}, {"another1": hero_another_name},
                                      {"another2": hero_another_name}, {"another3": hero_another_name},
                                      {"another4": hero_another_name}, {"another5": hero_another_name}]}):
        list_tmp.append(x)
    client.close()
    if len(list_tmp) > 0:
        return list_tmp[0]
    else:
        return None


"""
保存英雄排行
"""


def save_rank(rank_list):
    if db[mongo_config['HERO_RANK_TABLE']].insert(rank_list):
        print('存储成功！', str(rank_list))
        client.close()
        return True
    client.close()
    print('存储失败')
    return False


"""
如果输入英雄排行，则输出
"""


def lol_find_rank(day_time, position):
    search_set = db[mongo_config['HERO_RANK_TABLE']]
    list_tmp = []
    for x in search_set.find({'time': day_time, 'position': position}):
        list_tmp.append(x)
    client.close()
    if len(list_tmp) > 0:
        return list_tmp
    else:
        return None


def find_rank():
    search_set = db[mongo_config['MONGO_TABLE']]
    list_tmp1 = []
    for x in search_set.find({'day': '2019-06-19'}):
        list_tmp1.append(x)

    list_tmp2 = []
    for x in search_set.find({'day': '2019-06-21'}):
        list_tmp2.append(x)

    for i in range(0, 198):
        print(list_tmp1[i]['cn_name'], list_tmp2[i]['cn_name'])
    else:
        return None


def main():
    pass


if __name__ == '__main__':
    main()
