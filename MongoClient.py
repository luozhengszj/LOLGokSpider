# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     MonogoClient.py
   Author :        Luozheng
   date：          2019/6/28
-------------------------------------------------
   Change Activity:
                   2019/6/28:
-------------------------------------------------
Description :
全局mongo的操作模块
"""
__author__ = 'Luozheng'

import pymongo

import sys

sys.path.append('../')

from Config import mongo_config
from SpiderUtil.logUtil import Logger

log = Logger('../Log/MongoClient.log', level='debug')

client = pymongo.MongoClient(mongo_config['MONGO_URL'])
db = client[mongo_config['MONGO_DB']]


def user_find_type(user_id):
    search_set = db[mongo_config['USER_FIND_TYPE']]
    list_tmp = search_set.find_one({'user_id': user_id})
    if list_tmp:
        return list_tmp['game_type']
    return None


def insert_user_find_type(user_id, type):
    search_set = db[mongo_config['USER_FIND_TYPE']]
    list_tmp = search_set.insert_one({'user_id': user_id, 'game_type': type})
    if list_tmp:
        return 'success'
    return None


""""""


def update_user_find_type(user_id, type):
    search_set = db[mongo_config['USER_FIND_TYPE']]
    list_tmp = search_set.update_one({'user_id': user_id}, {'$set': {'game_type': type}})
    if list_tmp:
        return 'success'
    return None


"""
微信：保存关注者发送的消息
"""


def save_follower_to_mongo(follower_msg):
    if db[mongo_config['FOLLOWERS_TABLE']].insert(follower_msg):
        log.logger.debug('存储成功！' + str(follower_msg))
        return True
    log.logger.debug('存储失败！' + str(follower_msg))
    return False
