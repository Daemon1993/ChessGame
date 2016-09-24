
import Utils
from model import ResponseData

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
    #是否坐着
    isDown=None

    def __repr__(self):
        return 'userID :{0}'.format(self.userName)

    def __init__(self, userLink, userName):
        self.userLink = userLink
        self.userName = userName
        self.roomId = ""
        self.puke = ""
        self.userID = ""


    #前往某个房间
    def go2Room(self, room):
        user = room.getUserById(self.userLink)
        if user is not None:
            return False
        self.roomId = room.tag
        self.isDown=1
        room.addUser(self)

        print('user {0} join room {1}'.format(self.userName,room.tag))
        self.userLink.write_message('欢迎来到房间 {0}'.format(room.tag))
        return True

    # 离开房间
    def exitRoom(self):
        self.roomId = ""
        self.isDown=None

def newUser(userLink, userName):
    user = __User(userLink, userName)
    print("上线 " + user.userName )
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
        pukes = self.getPuke()

        for user in self.users:
            if user is None or user.isDown is None:
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

        user_count = len(self.users)
        data = ResponseData.RoomData.Data(1, 1, user_count, 4, 5, 10, 123, 100, 0)
        roomData = ResponseData.RoomData(10, 1, data)

        msg= Utils.parseSendJson(roomData)


        # ddd=json.loads(msg)
        # print(ddd['data'])

        # 便利发送user房间信息
        for user in self.users:
            self.senRoomMsg2User(msg, user)


    def senRoomMsg2User(self,json, user):
        user.userLink.write_message(json)

#房间加上Tag
def newRoom(tag):
    return __Room(tag)

