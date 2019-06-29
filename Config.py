# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Config.py
   Author :        Luozheng
   date：          2019/6/28
-------------------------------------------------
   Change Activity:
                   2019/6/28:
-------------------------------------------------
Description :
参数设置：包括了mongo设置、opgg、王者荣耀请求date等

"""
__author__ = 'Luozheng'

import datetime

opgg_config = {
    'OPGG_MAIN_URL': 'http://www.op.gg/champion/statistics',
    'OPGG_HERO_URL': 'http://www.op.gg/champion/',
    'OPGG_HERO_OPSITION_TOP': '/statistics/top',
    'OPGG_HERO_OPSITION_MID': '/statistics/mid',
    'OPGG_HERO_OPSITION_SUP': '/statistics/support',
    'OPGG_HERO_OPSITION_BOT': '/statistics/bot',
    'OPGG_HERO_OPSITION_JUG': '/statistics/jungle',
    'LOL_INSERT_TIME': datetime.datetime.now().strftime('%Y-%m-%d')
}

mongo_config = {
    'MONGO_URL': '127.0.0.1:27017',
    'MONGO_DB': 'opgg',
    'MONGO_TABLE': 'hero',
    'ANOTHER_NAME_TABLE': 'lol_hero_another',
    'FOLLOWERS_TABLE': 'wx_followers',
    'HERO_RANK_TABLE': 'hero_rank',
    'MONGO_GOK_TABLE': 'gok',
    'USER_FIND_TYPE': 'user_find_type',
}

xml_config = {
    'XML_FILE_PATH': 'hero_another_name.xml',
    'GOK_XML_FILE_PATH': 'gok_hero_another_name.xml'
}

web_config = {
    'HOST_IP': '127.0.0.1',
    'HOST_PORT': '5005'
}

"""
王者荣耀设置
"""
gok_config = {
    'GOK_GAME_ID': '20001',
    'GOK_VERSION': '3.1.96a',
    'APP_VERSION_NAME': '3.44.104',

    'HERO_RANK_URL': 'https://cgi.datamore.qq.com/datamore/smobahelper/v2/herorank',
    'HERO_Smobahelper': 'https://cgi.datamore.qq.com/datamore/smobahelper/v2/herorel?',

    'chrome_drive_path': '/home/sunny/wx/LOLGokEnv/chromedriver',

    'GOK_INSERT_TIME':datetime.datetime.now().strftime('%Y-%m-%d')
}
"""王者荣耀接口变更记录"""
gok_interface_log = {
    'post_data_20190623': {
        'userId': '58910302',
        'token': 'tPnDNBYf',
        'gameId': '20001',
        'openid': 'owanlsnfmzBfjurws3KxKpczmoA4',
        'gameOpenid': 'owanlsnfmzBfjurws3KxKpczmoA4',
        'channelId': '16000168',
    },
    'post_url_20190623': 'https://ssl.kohsocialapp.qq.com:10001/hero/getdetailranklistbyid',
    'post_smobahelper_url_20190623': 'https://ssl.kohsocialapp.qq.com:10001/hero/getheroextrainfo'
}
