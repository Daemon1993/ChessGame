import logging, json

import requests
import pprint

logger = logging.getLogger(__name__)


#统一解析
def parseAction(user_link, message):
    try:
        msg = json.loads(message)
    except Exception as e:
        logger.error('接收数据转换json失败')
        user_link.write_message(protocol['STATUSCODE']['REQ_ERROR'])
        return None

    code = msg['code']

    for code_key in action_dicts_from_c:
        if code == code_key:
            action_dicts_from_c[code_key].parseData(user_link=user_link, jsonObject=msg)
            break

#基类 处理 数据
class BaseAction:
    uid=0
    def parseData(self, user_link, jsonObject):
        logger.info('拿到dict基类对象')

#心跳处理
class Action8(BaseAction):
    def parseData(self, user_link, jsonObject):
        user_link.write_message(protocol['STATUSCODE']['OK'])

#testlogin
class Action11(BaseAction):
    def parseData(self, user_link, jsonObject):
        uid = jsonObject['uid']
        # logger.info(protocol)
        logger.info(uid)
        if isinstance(uid, int):
            user_link.write_message(protocol['STATUSCODE']['OK'])
        else:
            user_link.write_message(protocol['STATUSCODE']['REQ_ERROR'])

class Action1(BaseAction):
    def parseData(self, user_link, jsonObject):
        logger.info('code 1')
        user_link.write_message('code 1')


class Action2(BaseAction):
    def parseData(self, user_link, jsonObject):
        user_link.write_message('code 2')

# 添加 code  对应行为
def addAction(code, action):
    action_dicts_from_c[code] = action



# 行为协议 接受客户端
action_dicts_from_c = {}

protocol = {}

def initActionsFromC():
    reponse = requests.get("http://bg.huoor.com/PROTOCOL.json")
    global protocol
    try:
        protocol = json.loads(reponse.text)
    except:
        logger.error('json 数据异常 ')
        return

    pprint.pprint(protocol['DESCRIBE'])


    action1 = Action1()
    addAction(1, action1)

    action2 = Action2()
    addAction(2, action2)


    action8 = Action8()
    addAction(8, action8)

    action11 = Action11()
    addAction(11, action11)


        # ------------------------------分割线--------------------------#

        # 发送客户端
