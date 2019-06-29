# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     gokClass.py
   Author :        Luozheng
   date：          2019/6/28
-------------------------------------------------
   Change Activity:
                   2019/6/28:
-------------------------------------------------
Description :
王者荣耀的英雄类
{"gradeofrank":"1","heroid":"136","heroname":"武则天","herotypename":"法师","winpercent":"53.18",
"gameactpercnt":"2.43","herotype":"2","kda":"5.18","mvppercnt":"21.32"},

"""
__author__ = 'Luozheng'


class GokClass():
    # 20190623前
    """
    version = ''
    day = ''
    heroid = ''
    heroname = ''
    herotype = ''
    herotypename = ''
    winpercent = ''
    gameactpercnt = ''
    mvppercnt = ''
    kda = ''
    strongEnemy = []
    defeat = []
    victory = []
    skill = []
    zh_skill = ''
    mingwen = []
    first_build = []
    second_build = []
    """
    version = ''
    day = ''
    heroid = ''
    heroname = ''
    herotypename = ''
    herotype = ''
    tRank = ''
    winpercent = ''
    gameactpercnt = ''
    banRate = ''
    kengzhi = []
    beikengzhi = []
    skill = []
    zh_skill = ''
    mingwen = []
    first_build = []
    second_build = []

    def set_hero_type(self, type):
        self.herotype = type

    def convert_to_dict(self):
        dict = {}
        dict.update(self.__dict__)
        return dict

    def convert_to_dicts(self):
        obj_arr = []

        for o in self:
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)

        return obj_arr
