#对客户端的行为作出反应

action_dicts={}

#添加 code 对应行为
def addAction(code,action):
    action_dicts[code]=action


def action1(user_link):
    user_link.write_message('code 1')


def action2(user_link):
    print('code 2')

