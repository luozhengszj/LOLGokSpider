
## 爬取内容
> 可关注微信订阅号 loak 查看实际效果。
  * 实现对LOL官方数据查询网站[opgg](http://na.op.gg/champion/statistics)的数据（白金及以上），主要分析关于最新的英雄强势度胜率登场率排行、所走位置、召唤师技能、技能加点、出门装、神装、鞋子，及天赋加点，可根据英雄别名查询。
  * 实现王者荣耀官方数据爬取：
    * 来源一：王者荣耀英雄资料列表页 https://pvp.qq.com/web201605/herolist.shtml
    * 来源二：列表页内的英雄数据，爬取出装、加点等。如 曜 https://pvp.qq.com/web201605/herodetail/522.shtml
    * 来源三：王者营地关于英雄强势度、胜率、登场率、禁用率、英雄位置及类型、英雄克制

## 运行项目
  项目实现主要是基于 request、selenium作为爬取工具，pymongo作为操作MongoDB的模块，redis搭建的IP代理池，并将微信订阅号作为数据查询界面。因此实现该项目可参照以下步骤：
> **以下步骤遇到问题可参照博文 [爬虫实战（一）—利用requests、mongo、redis代理池爬取英雄联盟opgg实时英雄数据](https://blog.csdn.net/luoz_java/article/details/92741358) ，若有其他问题请联系或提交issue**：
  * 安装mongodb
  * 安装python3
  * clone本仓库
  * 安装必要模块：
    * 下载虚拟环境模块：pip3 install virtualenv
    * 创建虚拟环境：virtualenv LOLGokSpiderenv
    * 进入虚拟环境并激活：../LOLGokSpiderenv/Script/activite
    * 下载项目必要的模块：pip freeze > requirements.txt -i https://pypi.doubanio.com/simple/  （选择豆瓣源进行下载，速度很快）
  * 搭建IP代理池
    * 可以选择不搭建，但是要修改以下两个文件的内容（gokSelenium.py、opggSpider.py），将爬取代理代码删除即可。
    * 搭建代理池，可使用 jhao104 / proxy_pool 项目的代理池，搭建简单，直接装好redis，基本没什么问题。
  * 运行项目
 	虚拟环境下直接运行以下代码，使用代理的话，请确保代理池正在运行。
    * 运行LOL爬取
      python opggSpider.py
    * 运行王者荣耀爬取
      python gokSelenium.py

## 查看项目效果
> 可关注微信订阅号 loak 进行实际效果的查看。

> 想查看自己clone该项目的效果，可适当修改 SpiderUtil/wxMsgUtil.py下主函数代码进行测试。

## 有问题反馈
在使用中有任何问题，欢迎反馈给我，可以用以下联系方式跟我交流

* Email:864987080@qq.com
* Bolg: [@日出了的博客](https://richule.com)