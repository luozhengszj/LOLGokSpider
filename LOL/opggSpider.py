import re
import socket
import urllib.error
import datetime

import requests
from bs4 import BeautifulSoup

import sys
sys.path.append('../')

from Config import opgg_config
from LOL.heroClass import HeroClass, OPSITIONEnum
from LOL.lolMongoClient import save_to_mongo, save_rank

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.op.gg',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

# 发生错误的Url 以便排查
error_url = []

# 暂无数据的英雄
error_hero = []

# 获取opgg英雄的tier(各位置强势英雄 ：T1 T2 T3 T4等)
TOP_tier_dict = {}
JUG_tier_dict = {}
MID_tier_dict = {}
ADC_tier_dict = {}
SUP_tier_dict = {}


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").text


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get_all_hero():
    retry_count = 5
    proxy = get_proxy()
    while retry_count > 0:
        try:
            # 获取英雄列表
            proxies = {
                "http": "http://" + proxy
            }
            herohtml = requests.get(url=opgg_config['OPGG_MAIN_URL'], proxies=proxies, headers=headers, timeout=120).text
            # 存储所有英雄的hero对象
            list_hero = []
            soup = BeautifulSoup(herohtml, 'lxml')
            hero_items = soup.find_all(class_='champion-index__champion-item')
            hero_item_version = soup.select_one('[class~=champion-index__version]').text.split(':')[1].strip()

            for hero_item in hero_items:
                hero_en_name = hero_item['data-champion-key']
                hero_cn_name = hero_item['data-champion-name']
                hero_positions_items = hero_item.find_all(class_='champion-index__champion-item__position')
                hero_positions = []
                for hero_position in hero_positions_items:
                    hero_positions.append(hero_position.text)
                hero = HeroClass(hero_en_name, hero_cn_name, hero_positions, hero_item_version)
                list_hero.append(hero)

            # 没有足够取样的英雄
            hero_items = soup.find_all(class_='champion-index__champion-item__deceased')
            for hero_item in hero_items:
                hero_item_name = hero_item.previous_sibling.previous_sibling.text
                error_hero.append(hero_item_name)

            # 获取opgg英雄的tier(各位置强势英雄 ：T1 T2 T3 T4等)、胜率、登场率
            TOP_tier_dict.update({'version':hero_item_version, 'time': datetime.datetime.now().strftime('%Y-%m-%d'), 'position':'上单'})
            JUG_tier_dict.update(
                {'version': hero_item_version, 'time': datetime.datetime.now().strftime('%Y-%m-%d'), 'position': '打野'})
            MID_tier_dict.update(
                {'version': hero_item_version, 'time': datetime.datetime.now().strftime('%Y-%m-%d'), 'position': '中单'})
            ADC_tier_dict.update(
                {'version': hero_item_version, 'time': datetime.datetime.now().strftime('%Y-%m-%d'), 'position': 'Bottom'})
            SUP_tier_dict.update(
                {'version': hero_item_version, 'time': datetime.datetime.now().strftime('%Y-%m-%d'), 'position': '辅助'})
            get_all_hero_tier(soup)

            return list_hero
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                print(proxy + ' timeout')
                retry_count -= 1
                if retry_count == 2:
                    # 出错3次, 删除代理池中代理
                    delete_proxy(proxy)
                    proxy = get_proxy()
                    """
        except Exception as e:
            print(str(e))
            retry_count -= 1
            """
    return None


# 获取opgg英雄的tier(各位置强势英雄 ：T1 T2 T3 T4等)
# 获取opgg英雄胜率、登场率
def get_all_hero_tier(soup):

    hero_top_tier_tbody = soup.select('[class~=champion-trend-tier-TOP] > tr')
    for hero_top_tier_tbody_item in hero_top_tier_tbody:
        hero_iter_name = hero_top_tier_tbody_item.find(class_='champion-index-table__name').text
        hero_iter_win = hero_top_tier_tbody_item.select('[class~=champion-index-table__cell]')[4].text
        hero_iter_stage = hero_top_tier_tbody_item.select('[class~=champion-index-table__cell]')[5].text
        hero_iter_num = 'T' + re.search('icon-champtier-(.*)?\.png', hero_top_tier_tbody_item.select('img')[1]['src'],
                                        re.S).group(1)

        TOP_tier_dict.update({hero_iter_name:hero_iter_num + ' ' + hero_iter_win + ' ' + hero_iter_stage})
    print(TOP_tier_dict)

    hero_top_tier_tbody = soup.select('[class~=champion-trend-tier-JUNGLE] > tr')
    for hero_top_tier_tbody_item in hero_top_tier_tbody:
        hero_iter_name = hero_top_tier_tbody_item.find(class_='champion-index-table__name').text
        hero_iter_win = hero_top_tier_tbody_item.select('[class~=champion-index-table__cell]')[4].text
        hero_iter_stage = hero_top_tier_tbody_item.select('[class~=champion-index-table__cell]')[5].text
        hero_iter_num = 'T' + re.search('icon-champtier-(.*)?\.png', hero_top_tier_tbody_item.select('img')[1]['src'],
                                        re.S).group(1)
        JUG_tier_dict.update({hero_iter_name: hero_iter_num + ' ' + hero_iter_win + ' ' + hero_iter_stage})
    print(JUG_tier_dict)

    hero_top_tier_tbody = soup.select('[class~=champion-trend-tier-MID] > tr')
    for hero_top_tier_tbody_item in hero_top_tier_tbody:
        hero_iter_name = hero_top_tier_tbody_item.find(class_='champion-index-table__name').text
        hero_iter_win = hero_top_tier_tbody_item.select('[class~=champion-index-table__cell]')[4].text
        hero_iter_stage = hero_top_tier_tbody_item.select('[class~=champion-index-table__cell]')[5].text
        hero_iter_num = 'T' + re.search('icon-champtier-(.*)?\.png', hero_top_tier_tbody_item.select('img')[1]['src'],
                                        re.S).group(1)
        MID_tier_dict.update({hero_iter_name: hero_iter_num + ' ' + hero_iter_win + ' ' + hero_iter_stage})
    print(MID_tier_dict)

    hero_top_tier_tbody = soup.select('[class~=champion-trend-tier-ADC] > tr')
    for hero_top_tier_tbody_item in hero_top_tier_tbody:
        hero_iter_name = hero_top_tier_tbody_item.find(class_='champion-index-table__name').text
        hero_iter_win = hero_top_tier_tbody_item.select('[class~=champion-index-table__cell]')[4].text
        hero_iter_stage = hero_top_tier_tbody_item.select('[class~=champion-index-table__cell]')[5].text
        hero_iter_num = 'T' + re.search('icon-champtier-(.*)?\.png', hero_top_tier_tbody_item.select('img')[1]['src'],
                                        re.S).group(1)
        ADC_tier_dict.update({hero_iter_name: hero_iter_num + ' ' + hero_iter_win + ' ' + hero_iter_stage})
    print(ADC_tier_dict)

    hero_top_tier_tbody = soup.select('[class~=champion-trend-tier-SUPPORT] > tr')
    for hero_top_tier_tbody_item in hero_top_tier_tbody:
        hero_iter_name = hero_top_tier_tbody_item.find(class_='champion-index-table__name').text
        hero_iter_win = hero_top_tier_tbody_item.select('[class~=champion-index-table__cell]')[4].text
        hero_iter_stage = hero_top_tier_tbody_item.select('[class~=champion-index-table__cell]')[5].text
        hero_iter_num = 'T' + re.search('icon-champtier-(.*)?\.png', hero_top_tier_tbody_item.select('img')[1]['src'],
                                        re.S).group(1)
        SUP_tier_dict.update({hero_iter_name: hero_iter_num + ' ' + hero_iter_win + ' ' + hero_iter_stage})
    print(SUP_tier_dict)


def get_hero_detail(hero, opsition_url):
    print(opgg_config['OPGG_HERO_URL'] + hero.en_name + opsition_url)
    retry_count = 5
    proxy = get_proxy()
    while retry_count > 0:
        try:
            get_hero_detail_html = requests.get(opgg_config['OPGG_HERO_URL'] + hero.en_name + opsition_url,
                                                headers=headers, timeout=20).text
            soup = BeautifulSoup(get_hero_detail_html, 'lxml')

            hero_position_item = soup.select_one(
                '[class~=champion-stats-header__position--active] > a > [class~=champion-stats-header__position__rate]').text

            hero_position_list_tmp = [hero.hero_position, hero_position_item]
            hero.set_position(hero_position_list_tmp)

            hero_win = soup.select('[class~=champion-stats-trend-rank] > b')[0].text.strip()
            hero_win_num = soup.select('[class~=champion-stats-trend-rate]')[0].text.strip()

            hero_stage = soup.select('[class~=champion-stats-trend-rank] > b')[1].text.strip()
            hero_stage_num = soup.select('[class~=champion-stats-trend-rate]')[1].text.strip()

            hero_skill_items = soup.select('[class~=champion-stats__list] > li > [class~=tip]')
            hero_skill = []
            for result in hero_skill_items:
                tmp = re.search('<b .*?>(.*)?</b>', result['title'], re.S).group(1)
                hero_skill.append(tmp)

            hero_spell_items = soup.select('[class~=champion-skill-build__table] > tbody > tr > td')
            hero_spell = []
            for result in hero_spell_items:
                hero_spell.append(result.text.strip())

            # 装备
            hero_build_items = soup.select('[class~=champion-overview__data]')
            # 初始装备（第一套）
            hero_first_items = hero_build_items[3].select(
                '[class~=champion-stats__list] > [class~=champion-stats__list__item]')
            hero_first_build_one = []
            for result in hero_first_items:
                tmp = re.search('<b .*?>(.*)?</b>', result['title'], re.S).group(1)
                hero_first_build_one.append(tmp)
            # 初始装备（第二套）
            hero_first_build_two = []
            hero_first_items = hero_build_items[4].select(
                '[class~=champion-stats__list] > [class~=champion-stats__list__item]')
            for result in hero_first_items:
                tmp = re.search('<b .*?>(.*)?</b>', result['title'], re.S).group(1)
                hero_first_build_two.append(tmp)

            # 初始装备对用登场率、胜率
            hero_first_items_win = soup.select('[class~=champion-overview__stats--win]')[3].strong.text.strip()
            hero_first_items_stage = soup.select('[class~=champion-overview__stats--pick]')[3].strong.text.strip()
            hero_first_build_one.append(hero_first_items_win)
            hero_first_build_one.append(hero_first_items_stage)
            hero_first_items_win = soup.select('[class~=champion-overview__stats--win]')[4].strong.text.strip()
            hero_first_items_stage = soup.select('[class~=champion-overview__stats--pick]')[4].strong.text.strip()
            hero_first_build_two.append(hero_first_items_win)
            hero_first_build_two.append(hero_first_items_stage)

            # 最终装备，爬取三套
            hero_finally_items = hero_build_items[5].select(
                '[class~=champion-stats__list] > [class~=champion-stats__list__item]')
            hero_finally_build_one = []
            for result in hero_finally_items:
                tmp = re.search('<b .*?>(.*)?</b>', result['title'], re.S).group(1)
                hero_finally_build_one.append(tmp)

            hero_finally_build_two = []
            hero_finally_items = hero_build_items[6].select(
                '[class~=champion-stats__list] > [class~=champion-stats__list__item]')
            for result in hero_finally_items:
                tmp = re.search('<b .*?>(.*)?</b>', result['title'], re.S).group(1)
                hero_finally_build_two.append(tmp)

            hero_finally_build_thr = []
            hero_finally_items = hero_build_items[7].select(
                '[class~=champion-stats__list] > [class~=champion-stats__list__item]')
            for result in hero_finally_items:
                tmp = re.search('<b .*?>(.*)?</b>', result['title'], re.S).group(1)
                hero_finally_build_thr.append(tmp)

            # 最终装备对用登场率、胜率
            hero_finally_items_win = soup.select('[class~=champion-overview__stats--win]')[5].strong.text.strip()
            hero_finally_items_stage = soup.select('[class~=champion-overview__stats--pick]')[5].strong.text.strip()
            hero_finally_build_one.append(hero_finally_items_win)
            hero_finally_build_one.append(hero_finally_items_stage)
            hero_finally_items_win = soup.select('[class~=champion-overview__stats--win]')[6].strong.text.strip()
            hero_finally_items_stage = soup.select('[class~=champion-overview__stats--pick]')[6].strong.text.strip()
            hero_finally_build_two.append(hero_finally_items_win)
            hero_finally_build_two.append(hero_finally_items_stage)
            hero_finally_items_win = soup.select('[class~=champion-overview__stats--win]')[7].strong.text.strip()
            hero_finally_items_stage = soup.select('[class~=champion-overview__stats--pick]')[7].strong.text.strip()
            hero_finally_build_thr.append(hero_finally_items_win)
            hero_finally_build_thr.append(hero_finally_items_stage)

            # 鞋子，只爬取前两套
            hero_shoes_build_one = []
            hero_shoes_build_two = []
            # 排除蛇女
            if hero.en_name != 'cassiopeia':
                hero_shoes_items = hero_build_items[10].select(
                    '[class~=champion-stats__list] > [class~=champion-stats__list__item]')
                for result in hero_shoes_items:
                    tmp = re.search('<b .*?>(.*)?</b>', result['title'], re.S).group(1)
                    hero_shoes_build_one.append(tmp)
                hero_shoes_items_win = soup.select('[class~=champion-overview__stats--win]')[10].strong.text.strip()
                hero_shoes_items_stage = soup.select('[class~=champion-overview__stats--pick]')[10].strong.text.strip()
                hero_shoes_build_one.append(hero_shoes_items_win)
                hero_shoes_build_one.append(hero_shoes_items_stage)
                hero_shoes_items = hero_build_items[11].select(
                    '[class~=champion-stats__list] > [class~=champion-stats__list__item]')

                for result in hero_shoes_items:
                    tmp = re.search('<b .*?>(.*)?</b>', result['title'], re.S).group(1)
                    hero_shoes_build_two.append(tmp)
                hero_shoes_items_win = soup.select('[class~=champion-overview__stats--win]')[11].strong.text.strip()
                hero_shoes_items_stage = soup.select('[class~=champion-overview__stats--pick]')[11].strong.text.strip()
                hero_shoes_build_two.append(hero_shoes_items_win)
                hero_shoes_build_two.append(hero_shoes_items_stage)

            # 天赋爬取，两套
            hero_inborn_items = soup.select('[class~=champion-stats-summary-rune__name]')  # 两套天赋名称
            hero_inborn_items_num = soup.select('[class~=champion-stats-summary-rune__rate]')  # 两套天赋胜率、登场率
            hero_inborn_one = []
            hero_inborn_one.append(hero_inborn_items[0].text.strip())
            hero_inborn_two = []
            hero_inborn_two.append(hero_inborn_items[1].text.strip())

            hero_inborn_detail = soup.select('[class~=perk-page__item--active]')  # 两套天赋详细信息
            for inborn in hero_inborn_detail[:6]:
                hero_inborn_one.append(inborn.select_one('div > img')['alt'])
            hero_inborn_one.append(hero_inborn_items_num[0].select('span')[2].text.strip())  # 胜率
            hero_inborn_one.append(hero_inborn_items_num[0].select('strong')[0].text.strip())  # 登场率

            for inborn in hero_inborn_detail[6:12]:
                hero_inborn_two.append(inborn.select_one('div > img')['alt'])
            hero_inborn_two.append(hero_inborn_items_num[1].select('span')[2].text.strip())  # 胜率
            hero_inborn_two.append(hero_inborn_items_num[1].select('strong')[0].text.strip())  # 登场率

            hero.set_hero_detail(hero_win, hero_win_num, hero_stage, hero_stage_num, hero_skill, hero_spell,
                                 hero_first_build_one,hero_first_build_two, hero_finally_build_one,
                                 hero_finally_build_two, hero_finally_build_thr,
                                 hero_shoes_build_one, hero_shoes_build_two, hero_inborn_one, hero_inborn_two)
            return hero
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                print(proxy + ' timeout')
                retry_count -= 1
                if retry_count == 2:
                    # 出错3次, 删除代理池中代理
                    delete_proxy(proxy)
                    proxy = get_proxy()

        except Exception as e:
            print(str(e))
            retry_count -= 1
    error_url.append(opgg_config['OPGG_HERO_URL'] + hero.en_name + opsition_url)
    return None


def main():
    list_hero = get_all_hero()
    save_rank(TOP_tier_dict)
    save_rank(JUG_tier_dict)
    save_rank(MID_tier_dict)
    save_rank(ADC_tier_dict)
    save_rank(SUP_tier_dict)
    error_hero_num = []  # 记录失败的英雄顺序
    error_num = 0
    for hero in list_hero:
        for opsition in hero.hero_positions:
            hero.set_position(opsition)
            if OPSITIONEnum(opsition) == OPSITIONEnum.TOP:
                hero = get_hero_detail(hero, opgg_config['OPGG_HERO_OPSITION_TOP'])

            elif OPSITIONEnum(opsition) == OPSITIONEnum.MID:
                hero = get_hero_detail(hero, opgg_config['OPGG_HERO_OPSITION_MID'])

            elif OPSITIONEnum(opsition) == OPSITIONEnum.JUG:
                hero = get_hero_detail(hero, opgg_config['OPGG_HERO_OPSITION_JUG'])

            elif OPSITIONEnum(opsition) == OPSITIONEnum.BOT:
                hero = get_hero_detail(hero, opgg_config['OPGG_HERO_OPSITION_BOT'])
            else:
                hero = get_hero_detail(hero, opgg_config['OPGG_HERO_OPSITION_SUP'])

            if hero:
                print(hero.convert_to_dict())
                save_to_mongo(hero)
        error_num += 1
        if hero == None:
            error_hero_num.append(error_num)
    print(error_hero_num)
    print(error_url)

"""
    # 出错的处理
    print(error_hero[0])
    hero = list_hero[-5]
    opsition = hero.hero_positions[0]
    hero.set_position(opsition)
    if OPSITIONEnum(opsition) == OPSITIONEnum.TOP:
        hero = get_hero_detail(hero, opgg_config['OPGG_HERO_OPSITION_TOP'])

    elif OPSITIONEnum(opsition) == OPSITIONEnum.MID:
        hero = get_hero_detail(hero, opgg_config['OPGG_HERO_OPSITION_MID'])

    elif OPSITIONEnum(opsition) == OPSITIONEnum.JUG:
        hero = get_hero_detail(hero, opgg_config['OPGG_HERO_OPSITION_JUG'])

    elif OPSITIONEnum(opsition) == OPSITIONEnum.BOT:
        hero = get_hero_detail(hero, opgg_config['OPGG_HERO_OPSITION_BOT'])
    else:
        hero = get_hero_detail(hero, opgg_config['OPGG_HERO_OPSITION_SUP'])

    if hero:
        print(hero.convert_to_dict())
        save_to_mongo(hero)
    else:
        print('失败，已加入到error_list')
"""


if __name__ == '__main__':
    main()
