

import logging

logger = logging.getLogger(__name__)

#行为协议 接受客户端
action_dicts_from_c={}

#添加 code  对应行为
def addAction(code,action):
    action_dicts_from_c[code]=action


def action1(user_link):
    logger.info('code 1')
    user_link.write_message('code 1')


def action2(user_link):
    user_link.write_message('code 2')


def initActionsFromC():
    addAction(1, action1)
    addAction(2, action2)

#------------------------------分割线--------------------------#

#发送客户端


