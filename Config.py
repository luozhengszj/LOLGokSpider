opgg_config = {
    'OPGG_MAIN_URL': 'http://www.op.gg/champion/statistics',
    'OPGG_HERO_URL': 'http://www.op.gg/champion/',
    'OPGG_HERO_OPSITION_TOP': '/statistics/top',
    'OPGG_HERO_OPSITION_MID': '/statistics/mid',
    'OPGG_HERO_OPSITION_SUP': '/statistics/support',
    'OPGG_HERO_OPSITION_BOT': '/statistics/bot',
    'OPGG_HERO_OPSITION_JUG': '/statistics/jungle',
}

mongo_config = {
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

gok_config = {
    'GOK_GAME_ID': '20001',
    'GOK_VERSION': '3.1.96a',
    'APP_VERSION_NAME': '3.44.104',

    'HERO_RANK_URL': 'https://cgi.datamore.qq.com/datamore/smobahelper/v2/herorank',
    'HERO_Smobahelper':'https://cgi.datamore.qq.com/datamore/smobahelper/v2/herorel?'
}