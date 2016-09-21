import Presenter
import Utils

__author__ = 'Daemon1993'

'''
面向对象
每个功能 一个类
'''


# 用户类 里面有roomID
class __User():
    # 每个连接的WebSocket
    userLink = ""
    userName = ""
    roomId = ""
    #扑克牌具体数
    puke = ""
    userID=""

    def __repr__(self):
        return 'userID :{0}'.format(self.userName)

    def __init__(self, userLink, userName):
        self.userLink = userLink
        self.userName = userName
        self.roomId = ""
        self.puke = ""
        self.userLink = ""

    #前往某个房间
    def go2Room(self, room):
        user = room.getUserById(self.userLink)
        if user is not None:
            return False
        self.roomId = room.tag
        room.addUser(self)

        self.userLink.write_message('来到房间 {0}'.format(room.tag))
        return True

    # 离开房间
    def exitRoom(self):
        self.roomId = ""


def newUser(userLink, userName):
    user = __User(userLink, userName)
    print("上线 " + user.userName)
    return user


# 房间类 里面有User
class __Room():
    tag = ""
    users = []

    def __init__(self, tag):
        self.tag = tag
        self.users = []

    def addUser(self, user):
        self.users.append(user)
        return True

    def getUsers(self):
        return self.users

    def getUserSize(self):
        return len(self.users)

    def getUserById(self, userLink):
        for user in self.users:
            if user.userLink == userLink:
                return user
        return None

    # 给用户分发牌
    def showPuke(self):
        max = 0
        win_user = None
        pukes = Presenter.getPuke()

        for user in self.users:
            if user is None:
                continue
            puke = Utils.getRandomPuke(pukes)
            user.puke = puke
            realPuke = int(puke, 16)
            if realPuke > max:
                max = realPuke
                win_user = user
            print('showPuke {0} {1}'.format(user.userName, puke))
            user.userLink.write_message('你的牌 {0}'.format(puke))

        return win_user


def newRoom(tag):
    return __Room(tag)

