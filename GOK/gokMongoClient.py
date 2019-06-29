# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     gokMongoClient.py
   Author :        Luozheng
   date：          2019/6/28
-------------------------------------------------
   Change Activity:
                   2019/6/28:
-------------------------------------------------
Description :
王者荣耀操作mongo数据库的操作模块

"""
__author__ = 'Luozheng'

import datetime
import pymongo

import sys

sys.path.append('../')

from Config import mongo_config
from SpiderUtil.logUtil import Logger

client = pymongo.MongoClient(mongo_config['MONGO_URL'])
db = client[mongo_config['MONGO_DB']]

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

log = Logger('../Log/gokMongoClient.log', level='debug')

"""
爬取保存到MongoDB
"""


def gok_save_to_mongo(hero):
    if db[mongo_config['MONGO_GOK_TABLE']].update({'heroname': hero.heroname, 'day': datetime.datetime.now().strftime('%Y-%m-%d')}, {'$set': hero.convert_to_dict()}, True):
        log.logger.debug('存储成功！'+str(hero.heroname))
        return True
    log.logger.error('存储失败！'+str(hero.heroname))
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
    hero_one = search_set.find_one({'heroname': hero_name, 'day': yesterday.strftime('%Y-%m-%d')})

    client.close()
    if hero_one:
        return hero_one
    else:
        return None


def gok_get_herotypename(type):
    list_tmp = []
    search_set = db[mongo_config['MONGO_GOK_TABLE']]
    if type == '排行':
        set = search_set.find({'day': yesterday.strftime('%Y-%m-%d')}).sort('tRank')

        for x in set:
            list_tmp.append(x)
        client.close()
        return list_tmp[:40]
    elif type in ['射手', '辅助', '战士', '法师', '坦克', '刺客']:
        set = search_set.find({'$or': [{'herotypename': {'$regex': type}}, {'herotype': {'$regex': type}}],
                               'day': yesterday.strftime('%Y-%m-%d')}).sort([('tRank', 1), ('winpercent', -1)])
        for x in set:
            list_tmp.append(x)
        client.close()
        if len(list_tmp) > 30:
            return list_tmp[:30]
        return list_tmp
    else:
        set = search_set.find({'herotype': {'$regex': '.*' + type + '.*'}, 'day': yesterday.strftime('%Y-%m-%d')}).sort(
            'tRank')
        for x in set:
            list_tmp.append(x)
        client.close()
        if len(list_tmp) > 30:
            return list_tmp[:30]
        return list_tmp
