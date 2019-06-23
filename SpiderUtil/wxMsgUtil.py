import re
import datetime

from LOL.lolMongoClient import get_hero_name_by_another, \
    get_hero, lol_find_rank
from GOK.gokMongoClient import gok_get_hero, gok_get_herotypename
from MongoClient import user_find_type, insert_user_find_type, update_user_find_type, save_follower_to_mongo

lol_game = ['英雄联盟', 'LOL', 'lol', '撸啊撸']
gok_game = ['王者', '王者荣耀', '荣耀', '农药', '王者农药']
teshu_list = ['罗正', '说明']
game_list = lol_game + gok_game
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)


def hand_event():
    back_msg = '欢迎关注 英雄联盟 王者荣耀攻略\r\n\r\n初次关注请先输入查询的游戏名\r\n\r\n如【王者荣耀】、【LOL】'
    return back_msg


def hand_text_msg(xml_dict):
    user_content = clean_zh_text(xml_dict.get('Content'))
    user_content = ' '.join(user_content.split())
    back_msg = ''
    if len(user_content) < 10:
        user_id = xml_dict.get('FromUserName')
        game_type = user_find_type(user_id)
        if game_type:
            xml_dict.update({'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            xml_dict.pop('MsgId')
            xml_dict.pop('MsgType')
            xml_dict.pop('CreateTime')
            save_follower_to_mongo(xml_dict)
            if user_content not in lol_game and user_content not in gok_game:
                if user_content == '罗正':
                    back_msg = luozheng()
                elif game_type in lol_game:
                    if user_content == '说明':
                        back_msg = lolshuoming()
                    else:
                        back_msg = hand_lol(user_content)
                    return back_msg
                elif game_type in gok_game:
                    if user_content == '说明':
                        back_msg = gokshuoming()
                    else:
                        back_msg = hand_gok(user_content)
                    return back_msg

            else:
                if user_content in lol_game:
                    update_user_find_type(user_id, user_content)
                    back_msg = """切换 LOL 成功\r\n\r\n输入【排行 位置】查询位置英雄排行\r\n\r\n如【排行 上】可查看上路强势英雄\r\n\r\n输入【英雄名】查询英雄情况\r\n\r\n输入【英雄名 位置】查询英雄该位置玩法\r\n\r\n回复【说明】查看查询方法"""

                elif user_content in gok_game:
                    update_user_find_type(user_id, user_content)
                    back_msg = """切换 王者荣耀 成功\r\n\r\n输入【排行】查询前30英雄胜率\r\n\r\n如【类型】可查看类型强势英雄\r\n\r\n如输入【坦克】查询胜率前30坦克英雄\r\n\r\n可输入英雄名、刺客、坦克、射手、法师、辅助、排行\r\n\r\n回复【说明】查看查询方法"""
        else:
            # 用户未确定游戏类型
            if user_content in lol_game:
                insert_user_find_type(user_id, user_content)
                back_msg = """切换 LOL 成功\r\n\r\n输入【排行 位置】查询位置英雄排行\r\n\r\n如【排行 上】可查看上路强势英雄\r\n\r\n输入【英雄名】查询英雄情况\r\n\r\n输入【英雄名 位置】查询英雄该位置玩法"""

            elif user_content in gok_game:
                back_msg = """切换 王者荣耀 成功\r\n\r\n输入【排行】查询前30英雄胜率\r\n\r\n如【类型】可查看类型强势英雄\r\n\r\n如输入【坦克】查询胜率前30坦克英雄\r\n\r\n可输入英雄名、刺客、坦克、射手、法师、辅助、排行"""
            else:
                back_msg = """初次使用，请先确定类型\r\n\r\n请输入【王者荣耀】或【LOL】"""

            return back_msg

    else:
        back_msg = '请输入文字进行查询\r\n\r\n英雄联盟 王者荣耀 英雄全方位攻略\r\n\r\n回复【说明】查看查询方法'
        return back_msg
    return back_msg


def hand_lol(user_msg):
    user_msg = user_msg.split(' ')
    if len(user_msg) == 1:
        hero_another_name = get_hero_name_by_another(user_msg[0])
        if hero_another_name:
            hero_list = get_hero(hero_another_name['name'])
            return handle_hero_list_to_wx_msg(hero_list)
        else:
            return '英雄名输入有误\r\n\r\n可尝试【盖伦】'
    elif len(user_msg) > 1:
        user_msg = user_msg[:2]
        if (user_msg[0] == '排行'):
            check_flag = check_msg_position(user_msg[1])
            if check_flag == None:
                return None
            hero_rank = lol_find_rank(yesterday.strftime('%Y-%m-%d'), check_flag)
            if hero_rank and len(hero_rank) > 0:
                return handle_hero_rank_to_wx_msg(hero_rank)
            else:
                return '输入有误\r\n\r\n可尝试【排行 上路】'
        else:
            hero_another_name = get_hero_name_by_another(user_msg[0])
            if hero_another_name == None:
                return '英雄名输入有误\r\n\r\n可尝试【盖伦 上路】'
            hero_another_name = hero_another_name['name']
            hero_list = get_hero(hero_another_name)
            check_flag = check_msg_position(user_msg[1])
            if check_flag:
                if hero_list and len(hero_list) == 1:
                    return handle_hero_one_to_wx_msg(hero_list[0])
                elif len(hero_list) > 1:
                    for hero in reversed(hero_list):
                        if hero['hero_position'][0] == check_flag:
                            return handle_hero_one_to_wx_msg(hero)
                    return hero_another_name + '无此位置数据'
                else:
                    return hero_another_name + '数据暂时缺失'
            else:
                return '位置输入有误\r\n\r\n可尝试【盖伦 上路】'


def handle_hero_one_to_wx_msg(hero):
    line_feed = '\r\n'
    hero_name = hero['cn_name']
    hero_position_win_num = '胜率-登场率 ' + hero['hero_win_num'] + hero['hero_stage_num']
    hero_spell = '技能加点 ' + str(hero['hero_spell'])
    hero_inborn_one = '天赋1-登场率-胜率 ' + str(hero['hero_inborn_one'])
    hero_inborn_two = '天赋2-登场率-胜率 ' + str(hero['hero_inborn_one'])
    hero_first_build_one = '出门装1-胜率-登场率 ' + str(hero['hero_first_build_one'])
    hero_first_build_two = '出门装2-胜率-登场率 ' + str(hero['hero_first_build_two'])
    hero_finally_build_one = '后期装备1 ' + str(hero['hero_finally_build_one'])
    hero_finally_build_two = '后期装备2 ' + str(hero['hero_finally_build_two'])
    hero_finally_build_thr = '后期装备3 ' + str(hero['hero_finally_build_thr'])
    hero_skill = '召唤师技能 ' + str(hero['hero_skill'])
    hero_shoes_build_one = '鞋子1 ' + str(hero['hero_shoes_build_one'])
    hero_shoes_build_two = '鞋子1 ' + str(hero['hero_shoes_build_one'])
    return hero_name + line_feed + \
           hero_position_win_num + line_feed + \
           hero_spell + line_feed + \
           hero_inborn_one + line_feed + \
           hero_inborn_two + line_feed + \
           hero_first_build_one + line_feed + \
           hero_first_build_two + line_feed + \
           hero_finally_build_one + line_feed + \
           hero_finally_build_two + line_feed + \
           hero_finally_build_thr + line_feed + \
           hero_skill + line_feed + \
           hero_shoes_build_one + line_feed + \
           hero_shoes_build_two + line_feed


def handle_hero_list_to_wx_msg(hero_list):
    line_feed = '\r\n'
    hero_name = hero_list[-1]['cn_name']
    hero_position_win_num = '位置-胜率-登场率 ' + line_feed + line_feed
    for hero in hero_list:
        hero_position_win_num = hero_position_win_num + set_Bottom(hero['hero_position'][0]) + hero[
            'hero_win_num'] + hero['hero_position'][1] + line_feed
    other_msg = '来自opgg & 版本 ' + hero_list[-1]['hero_version'] + ' & 日期 ' + hero_list[-1]['day']
    back_msg = hero_name + line_feed + hero_position_win_num + line_feed + other_msg
    return back_msg


def handle_hero_rank_to_wx_msg(hero_rank):
    line_feed = '\r\n'
    hero_rank = hero_rank[0]
    hero_version = hero_rank['version']
    rank_time = hero_rank['time']
    hero_rank_str = '英雄—胜率—登场率：'
    back_msg = '版本 ' + hero_version + ' ' + rank_time + line_feed + hero_rank_str + line_feed + line_feed
    hero_rank.pop('_id')
    hero_rank.pop('position')
    hero_rank.pop('time')
    hero_rank.pop('version')
    for key, value in hero_rank.items():
        back_msg = back_msg + key + value + line_feed
    return back_msg


def set_ADC(position):
    if position == 'Bottom':
        return 'ADC'
    return position


def set_Bottom(position):
    if position == 'Bottom' or position == 'ad' or position == 'ADC' or position == 'AD' or position == 'adc':
        return 'Bottom'
    return position


def check_msg_position(position):
    if len(position) < 7:
        check_dict = {'上单': ['上单', '上', '上路'], '打野': ['打野', '野'], 'Bottom': ['bottom', 'ad', 'adc', 'AD', 'ADC', '下路'],
                      '中单': ['中', '中路', '中单'], '辅助': ['辅助', '辅', '下路']}
        for key, value in check_dict.items():
            for i in value:
                # 这里要注意报错
                if i == position.lower():
                    return key
    return None


def hand_gok(user_msg):
    user_msg = user_msg.split(' ')[0]
    # hero_another_name = get_hero_name_by_another(user_msg[0])
    if user_msg in ['射手', '辅助', '战士', '法师', '坦克', '刺客', '排行', '上路', '中路', '下路', '辅助', '打野']:
        # 默认胜率，取前30
        list_tmp = gok_get_herotypename(user_msg)
        return gok_handle_herotypename_to_wx_msg(list_tmp)

    else:
        hero_one = gok_get_hero(user_msg)
        if hero_one:
            return gok_handle_hero_to_wx_msg(hero_one)
        else:
            return '英雄名输入有误\r\n\r\n可尝试【牛魔】'


def gok_handle_hero_to_wx_msg(hero_one):
    line_feed = '\r\n'
    hero_name = hero_one['heroname'] + ' ' + hero_one['herotypename'] + line_feed + line_feed
    hero_position_win_num = '热度-胜率-登场率-MVP率-禁用率' + line_feed
    hero_position_win_num = hero_position_win_num + hero_one['tRank'] + '  ' + hero_one[
        'winpercent'] + '  ' + hero_one['gameactpercnt'] + '  ' + hero_one['banRate'] + line_feed + line_feed
    hero_skill = str(hero_one['skill']) + line_feed
    hero_zh_skill = '召唤师技能：' + hero_one['zh_skill'] + line_feed
    hero_mingwen = '铭文：' + " ".join(hero_one['mingwen']) + line_feed + line_feed
    hero_first_build = '出装一：' + "".join(hero_one['first_build']) + line_feed
    hero_second_build = '出装二：' + "".join(hero_one['second_build']) + line_feed + line_feed
    other_msg = '版本：' + hero_one['version'] + ' & 日期 ' + hero_one['day']

    other_msg_kengzhi_str = ''
    if len(hero_one['kengzhi']) > 1:
        other_msg_kengzhi_str = '克制：'
        for item in hero_one['kengzhi']:
            other_msg_kengzhi_str = other_msg_kengzhi_str + item['szTitle'] + ' ' + str(
                float(item.get('kzParam')) * 100)[:4] + '，'
        other_msg_kengzhi_str = other_msg_kengzhi_str[:-1] + line_feed
    other_msg_beikezhi_str = ''
    if len(hero_one['beikengzhi']) > 1:
        other_msg_beikezhi_str = '被克制：'
        for item in hero_one['beikengzhi']:
            other_msg_beikezhi_str = other_msg_beikezhi_str + item['szTitle'] + ' ' + str(
                float(item.get('bkzParam')) * 100)[
                                                                                      :4] + '，'
        other_msg_beikezhi_str = other_msg_beikezhi_str[:-1] + line_feed + line_feed
    back_msg = hero_name + hero_position_win_num + hero_position_win_num + hero_skill + hero_zh_skill + hero_mingwen + hero_first_build + hero_second_build + other_msg_kengzhi_str \
               + other_msg_beikezhi_str + other_msg
    return back_msg


def gok_handle_herotypename_to_wx_msg(hero_list):
    line_feed = '\r\n'
    msg_hero = '英雄 类型 热度 胜率|登场率' + line_feed + line_feed
    for hero in hero_list:
        msg_hero = msg_hero + hero['heroname'] + ' ' + hero['herotypename'] + ' ' + hero['tRank'] + ' ' + str(
            float(hero.get('winpercent')) * 100)[:4] + '|' + str(float(hero.get('gameactpercnt')) * 100)[:4] + line_feed
    msg = line_feed + '版本：' + hero_list[0]['version'] + '  日期：' + hero_list[0]['day']
    return msg_hero + msg


# make Chinese text clean
def clean_zh_text(text):
    # keep English, digital and Chinese
    comp = re.compile('[^A-Z^a-z^0-9^\u4e00-\u9fa5^ ]')
    return comp.sub('', text)


def lolshuoming():
    line_feed = '\r\n'
    back_msg = '订阅号可查询LOL、王者荣耀英雄数据' + line_feed + line_feed + '初次使用及切换查询需要输入【LOL】或【王者荣耀】' \
               + line_feed + line_feed + 'LOL 查询可输入别名' + line_feed + '输入【排行 位置】查询位置强势英雄' \
               + line_feed + '输入【英雄名】或查看英雄情况' + line_feed + '输入【英雄名 位置】查看详细攻略' + line_feed + 'LOL数据来自opgg' \
               + line_feed + line_feed + '欢迎到到个人网站:richule.com 交流'
    return back_msg


def gokshuoming():
    line_feed = '\r\n'
    back_msg = '订阅号可查询LOL、王者荣耀英雄数据' + line_feed + line_feed + '初次使用及切换查询需要输入【LOL】或【王者荣耀】' \
               + line_feed + line_feed + '王者荣耀 说明 ' + line_feed + '输入【英雄名】查看详细攻略' \
               + line_feed + '输入【胜率】或【类型】查看胜率前30英雄' + line_feed + '如【胜率】、【坦克】、【刺客】、【射手】、【辅助】、【法师】' \
               + line_feed + '王者数据来自官网' + line_feed + line_feed + '欢迎到到个人网站:richule.com 交流'
    return back_msg


def luozheng():
    line_feed = '\r\n'
    back_msg = '个人网站：richule.com' + line_feed + line_feed + 'Python Java C# 安卓 Web' \
               + line_feed + line_feed + '爬虫 图像识别 数据可视化分析等' \
               + line_feed + line_feed + '欢迎到到个人网站交流'
    return back_msg


if __name__ == '__main__':
    import xmltodict

    xml = """
        <xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName>12345</FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType>盖伦</MsgType>
    <Content>战士</Content>
    <MsgId>LOL</MsgId>
    </xml>
       """
    xml_dict = xmltodict.parse(xml)
    xml_dict = xml_dict.get("xml")
    msg_type = xml_dict.get("MsgType")
    back_msg = hand_text_msg(xml_dict)
    print(back_msg)
