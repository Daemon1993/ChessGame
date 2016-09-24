#统一判断数据解析 该干什么
__author__ = 'Daemon1993'
import json



#解析传来数据 指向不同的行为
def parseAction(user_link,json_msg,action_dict):
    print(json_msg)
    try:
        msg=json.loads(json_msg)
    except Exception as e:
        print('接收数据转换json失败')
        return None

    code=msg['code']

    for code_key in action_dict:
        if code==code_key:
            action_dict[code_key](user_link)
            break


#生成json 传给客户端
def parseSendJson(obj):
    msg = json.dumps(obj, ensure_ascii=False, default=serialize_instance)
    return msg


def serialize_instance(obj):
    d = {}
    d.update(vars(obj))
    return d
