from enum import Enum, unique
import datetime

"""
mongodb中存储的是hero 某个位置的对象对应信息：
例如：齐天大圣，在Mongo中是两条记录，打野和上单各一条。
HeroClass类
hero_position  记录对应的英雄位置、比例
hero_version  记录对应的LOL版本
hero_win  英雄在该位置上对应的胜率排行
hero_win_num  英雄在该位置上对应的胜率
hero_stage  英雄在该位置上对应的登场率排行
hero_stage  英雄在该位置上对应的登场率
hero_skill  英雄在该位置上常带的两套召唤师节能
hero_spell  英雄在该位置上的技能加点
hero_first_build_one  英雄在该位置上的首选出门装备、胜率、登场率
hero_first_build_two  英雄在该位置上的次选出门装备、胜率、登场率
hero_spell  英雄在该位置上的技能加点
"""
class HeroClass:
    hero_position = []

    hero_version = ''

    hero_win = 50
    hero_win_num = 0.5
    hero_stage = 50
    hero_stage_num = 0.05
    hero_skill = []
    hero_spell = []
    hero_first_build_one = []
    hero_first_build_two = []
    hero_finally_build_one = []
    hero_finally_build_two = []
    hero_finally_build_thr = []
    hero_shoes_build_one = []
    hero_shoes_build_two = []
    hero_inborn_one = []
    hero_inborn_two = []

    def __init__(self, en_name, cn_name, hero_positions, hero_version):
        self.en_name = en_name
        self.cn_name = cn_name
        self.hero_version = hero_version
        self.hero_positions = hero_positions
        self.day = datetime.datetime.now().strftime('%Y-%m-%d')

    def __str__(self):
        return 'en_name:' + self.en_name + '  cn_name:' + self.cn_name + '  hero_positions:' + \
               str(self.hero_positions)+'  hero_position:' + str(self.hero_position) + '  hero_version:' + self.hero_version\
               + 'en_name:' + self.en_name + '  cn_name:' + self.cn_name + '  hero_positions:' + self.hero_positions + \
               '  hero_win:' + self.hero_win + '  hero_win_num:' + self.hero_win_num + '  hero_stage:' + \
               self.hero_stage + '  hero_stage_num:' + self.hero_stage_num + \
               '  hero_skill:' + str(self.hero_skill) + '  hero_spell:' + str(self.hero_spell) + \
               '  hero_first_build_one:' + str(self.hero_first_build_one) + '  hero_first_build_two:' + \
               str(self.hero_first_build_two) + '  hero_finally_build_one:' + str(self.hero_finally_build_one) + \
               '  hero_finally_build_two:' + str(self.hero_finally_build_two) + '  hero_shoes_build:' + \
               str(self.hero_shoes_build)

    def set_hero_detail(self, hero_win, hero_win_num, hero_stage, hero_stage_num, hero_skill, hero_spell,
                        hero_first_build_one,
                        hero_first_build_two, hero_finally_build_one, hero_finally_build_two, hero_finally_build_thr,
                        hero_shoes_build_one, hero_shoes_build_two, hero_inborn_one, hero_inborn_two):
        self.hero_win = hero_win
        self.hero_win_num = hero_win_num
        self.hero_stage = hero_stage
        self.hero_stage_num = hero_stage_num
        self.hero_skill = hero_skill
        self.hero_spell = hero_spell
        self.hero_first_build_one = hero_first_build_one
        self.hero_first_build_two = hero_first_build_two
        self.hero_finally_build_one = hero_finally_build_one
        self.hero_finally_build_two = hero_finally_build_two
        self.hero_finally_build_thr = hero_finally_build_thr
        self.hero_shoes_build_one = hero_shoes_build_one
        self.hero_shoes_build_two = hero_shoes_build_two
        self.hero_inborn_one = hero_inborn_one
        self.hero_inborn_two = hero_inborn_two

    def set_position(self, hero_position):
        self.hero_position = hero_position

    def convert_to_dict(self):
        dict = {}
        dict.update(self.__dict__)
        return dict

    def convert_to_dicts(self):
        obj_arr = []

        for o in self:
            # 把hero对象转换成Dict对象
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)

        return obj_arr


@unique
class OPSITIONEnum(Enum):
    TOP = '上单'
    MID = '中单'
    JUG = '打野'
    SUP = '辅助'
    BOT = 'Bottom'
