import Presenter
import Utils

__author__ = 'Daemon1993'

'''
面向对象
每个功能 一个类
'''


# 用户类
class __User():
    #userID是每个连接的WebSocket
    userId = ""
    userName = ""
    roomId = ""
    puke=""


    def __str__(self):
        return 'userID :{0}'.format(self.userId)

    def __init__(self, userId, userName):
        self.userId = userId
        self.userName = userName
        self.roomId=""
        self.puke=""


    #前往某个房间
    def go2Room(self, room):
        user=room.getUserById(self.userId)
        if user is not None:
            return False
        self.roomId = room.tag
        room.addUser(self)

        self.userId.write_message('来到房间 {0}'.format(room.tag))
        return True

    #离开房间
    def exitRoom(self):
        self.roomId=""


def newUser(userId, userName):
    user = __User(userId, userName)
    print("newUser " + user.userName)
    return user


# 房间类
class __Room():
    tag = ""
    users = []

    def __init__(self, tag):
        self.tag = tag
        self.users=[]

    def addUser(self, user):
        self.users.append(user)
        return True

    def getUsers(self):
        return self.users

    def getUserSize(self):
        return len(self.users)

    def getUserById(self,userId):
        for user in self.users:
            if user.userId == userId:
                return user
        return None

    #给用户分发牌
    def showPuke(self):
        max=0
        win_user=None
        pukes = Presenter.getPuke()

        for user in self.users:
            puke=Utils.getRandomPuke(pukes)
            user.puke=puke
            realPuke=int(puke,16)
            if realPuke>max:
                max=realPuke
                win_user=user
            print('showPuke {0} {1}'.format(user.userName,puke))
            user.userId.write_message('你的牌 {0}'.format(puke))

        return win_user




def newRoom(tag):
    return __Room(tag)

# --------------------------------分割线------------------------------------#
