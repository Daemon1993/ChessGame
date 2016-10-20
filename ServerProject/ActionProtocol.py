import logging, json

import requests
import pprint
import Presenter

logger = logging.getLogger(__name__)

STATUSCODE = "STATUSCODE"
REQ_ERROR = "REQ_ERROR"
ERROR = "ERROR"

OK = "OK"
STATUS = "status"

STRUCTURE = "STRUCTURE"

DESCRIBE = "DESCRIBE"


# 统一解析
def parseAction(user_link, message):
    try:
        msg = json.loads(message)
    except Exception as e:
        logger.error('接收数据转换json失败')
        user_link.write_message(protocol[STATUSCODE][REQ_ERROR])
        return None

    code = msg['code']

    for code_key in action_dicts_from_c:
        if code == code_key:
            action_dicts_from_c[code_key].parseData(user_link=user_link, jsonObject=msg, code=str(code + 1))
            break

# 基类 处理 数据
class BaseAction:
    def __init__(self):
        self.datas = dict(STATUS=ERROR)

    def parseData(self, user_link, jsonObject, code):
        self.datas.update(STATUS=ERROR)
        logger.info('拿到dict基类对象')

    # 返回正确信息
    def ok_common(self, user_link):
        user_link.write_message(json.dumps(self.datas))

    # 返回错误信息
    def error_common(self, user_link, type):
        user_link.write_message(json.dumps(self.datas.update(STATUS=type)))


# 心跳处理
class Action8(BaseAction):
    def parseData(self, user_link, jsonObject, code):
        user_link.write_message(protocol[STATUSCODE][OK])


# testlogin
class Action11(BaseAction):
    def parseData(self, user_link, jsonObject, code):
        uid = jsonObject['uid']
        # logger.info(protocol)
        logger.info(uid)

        if isinstance(uid, int):
            Presenter.userManager.addUser(user_link, str(uid), uid)
            self.datas.update(STATUS=OK)
            self.ok_common(user_link)
        else:
            self.error_common(user_link, REQ_ERROR)


class Action1(BaseAction):
    def parseData(self, user_link, jsonObject, code):
        uid = jsonObject['uid']
        rid = jsonObject['rid']

        if isinstance(uid, int) and isinstance(rid, int):
            user = Presenter.userManager.getUserByUid(uid)
            logger.debug("Action1 {0}".format(user))

            if user is None:
                self.error_common(user_link, ERROR)
                return

            room = Presenter.roomManager.getRoomByTag(rid)

            logger.debug("Action1 {0}".format(room))

            if room is None:
                self.error_common(user_link, ERROR)
                return

            Presenter.joinRoom(user, room)

        else:
            self.error_common(user_link, REQ_ERROR)


class Action2(BaseAction):
    def parseData(self, user_link, jsonObject, code):
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

    pprint.pprint(protocol[DESCRIBE])

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
