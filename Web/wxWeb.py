import sys
import time

import xmltodict
from flask import Flask, request

sys.path.append('../')

from SpiderUtil.wxMsgUtil import hand_event, hand_text_msg


app = Flask(__name__)


@app.route('/loak', methods=["GET", "POST"])
def get_user_msg_from_wx():
    if request.method == "POST":
        xml_str = request.data
        if not xml_str:
            return ""
        xml_OrderedDict = xmltodict.parse(xml_str)
        xml_dict = xml_OrderedDict.get("xml")
        msg_type = xml_dict.get("MsgType")

        print(msg_type)
        back_msg = ''
        if msg_type == "text":
            back_msg = hand_text_msg(xml_dict)
        elif msg_type == "event":
            back_msg = hand_event()
        else:
            back_msg = '请输入文字进行查询\r\n\r\n英雄联盟 王者荣耀 英雄全方位攻略\r\n\r\n回复【说明】查看查询方法'

        resp_dict = {
            "xml": {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": back_msg
            }
        }
        resp_xml_str = xmltodict.unparse(resp_dict)
        # 返回消息数据给微信服务器
        return resp_xml_str


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5005)
