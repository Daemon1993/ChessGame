#统一判断数据解析 该干什么
__author__ = 'Daemon1993'
import json


#
def action1():
    pass


def action2():
    pass


#解析传来数据
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


#生成json 传给客户端
def parseSendJson(obj):
    msg = json.dumps(obj, ensure_ascii=False, default=serialize_instance)
    return msg


def serialize_instance(obj):
    d = {}
    d.update(vars(obj))
    return d
