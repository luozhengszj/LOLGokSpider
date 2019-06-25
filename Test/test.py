from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import socket
import urllib.error
import datetime
import ast
import sys

sys.path.append('../')
from Config import gok_interface_log, gok_config

import time
import requests
from GOK.gokClass import GokClass
from GOK.gokMongoClient import gok_save_to_mongo

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option('excludeSwitches',
                                       ['enable-automation'])
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)

hero_list = []
hero_url_list = {}
wait = WebDriverWait(browser, 10)
gok_version = ''


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").text


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get_all_url():
    try_num = 3

    proxy = get_proxy()
    chrome_options.add_argument('--proxy-server=http://' + proxy)

    browser.get("https://pvp.qq.com/web201605/herolist.shtml")

    while try_num > 0:
        try:
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                'body > div.wrapper > div > div > div.herolist-box > div.herolist-content > ul > li:nth-child(1) > a')))
            all_hero_items = browser.find_elements_by_css_selector(
                'body > div.wrapper > div > div > div.herolist-box > div.herolist-content > ul > li')
            for hero_item in all_hero_items:
                hero_url = hero_item.find_element_by_tag_name('a').get_attribute('href')
                hero_url_name = hero_item.find_element_by_tag_name('img').get_attribute('alt')
                hero_url_list.update({hero_url_name:hero_url})
            browser.get("https://pvp.qq.com/cp/a20170829bbgxsm/index.html")
            gok_version = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                'body > div.wrapper > div.container > ul > li:nth-child(1) > div > p'))).text.split(
                '：')[1].replace('.', '-')

            return hero_url_list, gok_version
        except TimeoutException as e:
            print(str(e))
            try_num -= 1
            delete_proxy(proxy)
            proxy = get_proxy()
            chrome_options.add_argument('--proxy-server=http://' + proxy)
            browser.get("https://pvp.qq.com/web201605/herolist.shtml")
    return hero_url_list


def get_one_hero_detail(hero_url, gok_hero):
    proxy = get_proxy()
    chrome_options.add_argument('--proxy-server=http://' + proxy)
    browser.get(hero_url)

    tmp1 = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[2]/p[1]/span'))).text
    tmp2 = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[1]/div[2]/p[3]/span').text
    gok_hero.skill = ['主：' + tmp1, '副：' + tmp2]

    zh_skill = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[1]/div[2]/p[5]/span').text
    gok_hero.zh_skill = zh_skill

    mingwen1 = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[3]/div[2]/ul/li[1]/p[1]/em').text
    mingwen2 = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[3]/div[2]/ul/li[2]/p[1]/em').text
    mingwen3 = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[3]/div[2]/ul/li[3]/p[1]/em').text
    gok_hero.mingwen = [mingwen1, mingwen2, mingwen3]

    browser.implicitly_wait(5)
    builds = browser.find_elements_by_xpath('//*[@id="Jname"]')
    list_tmp = []
    for item in builds:
        list_tmp.append(item.get_attribute("innerHTML"))
    gok_hero.first_build = list_tmp[:6]
    gok_hero.second_build = list_tmp[6:12]

    print(gok_hero.convert_to_dict())
    time.sleep(1)
    return gok_hero


""" --------------------------------------------------------"""

all_hero_msg = []


def get_hero_rank(lu):
    retry_count = 3
    proxy = get_proxy()
    while retry_count > 0:
        try:
            # 获取英雄列表
            proxies = {
                "http": "http://" + proxy
            }
            data_tmp = gok_interface_log['post_data_20190623']
            data_tmp.update({'position': lu})
            herohtml = requests.post(url=gok_interface_log['post_url_20190623'],
                                     data=data_tmp,
                                     proxies=proxies).text
            return herohtml
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                print(proxy + ' timeout')
                retry_count -= 1
                if retry_count == 1:
                    # 出错3次, 删除代理池中代理
                    delete_proxy(proxy)
                    proxy = get_proxy()
        except Exception as e:
            print(str(e))
            retry_count -= 1
    return None


def parse_hero_rank(rank_data, version, position):
    rank_data = ast.literal_eval(rank_data)
    hero_rank_list = str(rank_data.get('data').get('list'))[1:-1]
    hero_items = ast.literal_eval(hero_rank_list)
    for item in hero_items:
        gok = GokClass()
        gok.version = version
        gok.day = gok_config['GOK_INSERT_TIME']
        gok.heroid = item['heroId']
        gok.heroname = item['heroInfo'][0]['heroName']
        gok.herotype = position  # 英雄走哪路
        gok.herotypename = item['heroInfo'][0]['heroCareer']
        gok.tRank = item['tRank']
        gok.winpercent = item['winRate']
        gok.gameactpercnt = item['showRate']
        gok.banRate = item['banRate']
        all_hero_msg.append(gok)


def get_hero_smobahelper(hero_id):
    retry_count = 3
    proxy = get_proxy()
    while retry_count > 0:
        try:
            # 获取英雄列表
            proxies = {
                "http": "http://" + proxy
            }
            data_tmp = gok_interface_log['post_data_20190623']
            data_tmp.update({'heroId': hero_id})
            hero_smobahelper = requests.post(
                url=gok_interface_log['post_smobahelper_url_20190623'],data=data_tmp,
                proxies=proxies).text
            return hero_smobahelper
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                print(proxy + ' timeout')
                retry_count -= 1
                if retry_count == 1:
                    # 出错3次, 删除代理池中代理
                    delete_proxy(proxy)
                    proxy = get_proxy()
        except Exception as e:
            print(str(e))
            retry_count -= 1
    return None


def parse_hero_rank_smobahelper(hero_smobahelper, hero_tmp):
    rank_smobahelper = ast.literal_eval(hero_smobahelper.encode('utf-8').decode('unicode_escape').replace('/','').replace('null', "''"))
    beikengzhi1 = rank_smobahelper.get('data').get('bkzInfo').get('list')
    hero_tmp.beikengzhi = beikengzhi1
    kengzhi1 = rank_smobahelper.get('data').get('kzInfo').get('list')
    hero_tmp.kengzhi = kengzhi1
    return hero_tmp


def main():
    hero_position_dict = {}
    hero_url_list, version = get_all_url()

    i = 1
    for position in ['上路', '中路', '下路', '辅助', '打野']:
        hero_rank = get_hero_rank(i)
        parse_hero_rank(hero_rank, version, position)
        i += 1

    for item in all_hero_msg:
        if hero_url_list.get(item.heroname):
            hero_smobahelper = get_hero_smobahelper(item.heroid)
            hero_smobahelper_new = parse_hero_rank_smobahelper(hero_smobahelper, item)
            new_hero = get_one_hero_detail(hero_url_list.get(item.heroname), hero_smobahelper_new)

            if hero_position_dict.get(new_hero.heroname):
                new_postion = hero_position_dict.get(new_hero.heroname)+' '+new_hero.herotype
                hero_position_dict.update({item.heroname:new_postion})
                new_hero.set_hero_type(new_postion)
                print(new_hero.convert_to_dict())
            else:
                hero_position_dict.update({item.heroname:item.herotype})
            print('hero_position_dict', str(hero_position_dict))
            gok_save_to_mongo(new_hero)


    browser.close()


if __name__ == '__main__':
    main()
    if browser:
        browser.close()
