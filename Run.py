# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Run.py
   Author :        Luozheng
   date：          2019/6/28
-------------------------------------------------
   Change Activity:
                   2019/6/28:
-------------------------------------------------
Description :
开启爬取
"""
__author__ = 'Luozheng'

from GOK.gokSelenium import main as gok_main
from LOL.opggSpider import main as lol_main

if __name__ == '__main__':
    gok_main()
    lol_main()