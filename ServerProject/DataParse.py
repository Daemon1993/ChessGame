#统一判断数据解析 该干什么
__author__ = 'Daemon1993'
import json


#
def action1():
    pass


def action2():
    pass


def parseAction(json_msg):

    try:
        msg=json.loads(json_msg)
    except Exception as e:
        print('接收数据转换json失败')
        return None


    code=msg['code']
    if code==1:
        action1()
        return
    if code==2:
        action2()
        return

