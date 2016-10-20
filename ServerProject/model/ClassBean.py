import Utils
from model import ResponseData

__author__ = 'Daemon1993'
import logging

logger = logging.getLogger(__name__)

'''
面向对象
每个功能 一个类
'''


# 用户类 里面有roomID
class __User():
    # # 每个连接的WebSocket
    # userLink = ""

    def __repr__(self):
        return 'userID :{0}'.format(self.userName)

    def __init__(self, userLink, userName, uid):
        self.userLink = userLink
        self.userName = userName
        self.roomId = ""
        self.puke = []
        self.uid = uid
        self.isDown = False

    # 前往某个房间
    def go2Room(self, room):
        user = room.getUserById(self.uid)
        if user is not None:
            return False
        self.roomId = room.tag
        self.isDown = True
        room.hasSeats += 1

        room.addUser(self)

        logger.info('user {0} join room {1}'.format(self.userName, room.tag))

        self.userLink.write_message('欢迎来到房间 {0}'.format(room.tag))
        return True

    # 前往座位
    def getSeat(self, room):
        if room.hasSeats >= 100:
            logger.warning('座位已满 不能继续坐下')
            return
        self.isDown = True

    # 离开房间
    def exitRoom(self, room):
        # 房间清除
        room.users.remove(self)

        self.roomId = ""
        self.isDown = None
        self.isDown = False


def newUser(userLink, userName, uid):
    user = __User(userLink, userName, uid)
    logger.info("上线 " + user.userName)
    return user


# 房间类 里面有User
class __Room():
    def __init__(self, tag):
        # tag is  rid
        self.roomSeatCount = 4
        self.tag = tag
        self.users = []
        self.hasSeats = 0
        logger.debug("create room {0}".format(tag))

    def addUser(self, user):
        self.users.append(user)
        return True

    def getUsers(self):
        return self.users

    def getUserSize(self):
        return len(self.users)

    def getUserById(self, uid):
        for user in self.users:
            if user.uid == uid:
                return user
        return None

    # 给用户分发牌
    def showPuke(self):
        pukes = self.getPuke()
        for user in self.users:
            if user is None or user.isDown is None:
                continue
            puke = Utils.getRandomPuke(pukes)
            user.puke.append(puke)
            user.puke.append(puke)

    # 获取扑克牌 每次新的
    def getPuke(self):
        pukes = []
        # 16进制 52张牌
        pukes.clear()
        for index in range(1, 14):
            a = index + 16
            b = index + 32
            c = index + 48
            d = index + 64
            pukes.append(hex(a))
            pukes.append(hex(b))
            pukes.append(hex(c))
            pukes.append(hex(d))
        return pukes

    def updateRoom(self):

        seats = []
        for user in self.users:
            if user.isDown:
                self.showPuke()
                seat=ResponseData.JoinRoom.Seat(user.uid,user.puke)
                seats.append(seat)

        roomData = ResponseData.JoinRoom(self.tag, 1, 1,seats)

        msg = Utils.parseSendJson(roomData)

        # 便利发送user房间信息
        for user in self.users:
            self.senRoomMsg2User(msg, user)

    def senRoomMsg2User(self, json, user):
        user.userLink.write_message(json)


# 房间加上Tag
def newRoom(tag):
    return __Room(tag)
