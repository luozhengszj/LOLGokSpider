import datetime
import pymongo

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
def gok_save_to_mongo(hero):
    if db[mongo_config['MONGO_GOK_TABLE']].insert(hero.convert_to_dict()):
        print('存储成功！', str(hero.convert_to_dict()))
        return True
    print('存储失败')
    client.close()
    return False


"""
获取所有英雄
"""
def gok_get_all_hero():
    search_set = db[mongo_config['MONGO_GOK_TABLE']]
    list_tmp = []
    for x in search_set.find():
        list_tmp.append(x)

    client.close()
    if len(list_tmp) > 0:
        return list_tmp
    else:
        return None


def gok_get_hero(hero_name):
    search_set = db[mongo_config['MONGO_GOK_TABLE']]
    hero_one = search_set.find_one({'heroname':hero_name, 'day':yesterday.strftime('%Y-%m-%d')})

    client.close()
    if hero_one:
        return hero_one
    else:
        return None

def gok_get_herotypename(type):
    list_tmp = []
    search_set = db[mongo_config['MONGO_GOK_TABLE']]
    if type =='排行':
        set = search_set.find({'day':yesterday.strftime('%Y-%m-%d')}).sort('tRank')

        for x in set:
            list_tmp.append(x)
        client.close()
        return list_tmp[:40]
    elif type in ['射手', '辅助', '战士', '法师', '坦克', '刺客']:
        set = search_set.find({'herotypename':type,'day': yesterday.strftime('%Y-%m-%d')}).sort('tRank')
        for x in set:
            list_tmp.append(x)
        client.close()
        if len(list_tmp) > 30:
            return list_tmp[:30]
        return list_tmp
    else:
        set = search_set.find({'herotype': type, 'day': yesterday.strftime('%Y-%m-%d')}).sort('tRank')
        for x in set:
            list_tmp.append(x)
        client.close()
        if len(list_tmp) > 30:
            return list_tmp[:30]
        return list_tmp

