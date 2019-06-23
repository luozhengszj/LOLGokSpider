import pymongo

import sys
sys.path.append('../')

from Config import mongo_config

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
        print('存储成功！', str(follower_msg))
        return True
    print('存储失败')
    return False


