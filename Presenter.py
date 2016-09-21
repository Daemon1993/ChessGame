import Utils
import model.ResponseData

__author__ = 'Daemon1993'

import ClassBean
import json


'''
主持人 逻辑控制者
'''
pukes = []


def initData(size):
    # 初始化 房间数
    for index in range(1, size+1):
        roomTag = "room" + str(index)
        roomManager.newRoom(roomTag)

    print('all room {0}'.format(len(roomManager.managers)))


# 获取扑克牌 每次新的
def getPuke():
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


# 开始 puke
def disTributePuke(room):
    win_user = room.showPuke()

    for user in room.users:
        if win_user.userLink == user.userLink:
            win_user.userLink.write_message('win 你赢了')
        else:
            user.userLink.write_message('win 你输了 赢家{0}'.format(win_user.puke))


# 用户集合管理
class __UserManager():
    # dict link-user
    users = {}

    def addUser(self, userLink, userName):
        user = self.users.get(userLink)
        if user is not None:
            print('用户已经存在')
        else:
            user = ClassBean.newUser(userLink, userName)

        self.users[userLink] = user
        return user

    def getUserSize(self):
        return len(self.users)

    # 用户下线
    def removeUser(self, userLink):
        user=self.users[userLink]
        print("掉线 {0}".format(user))

        # 删除当前账号的房间的当前用户
        roomManager.removeUserById(user)

        del self.users[userLink]

        print(len(self.users))


userManager = __UserManager()


# 房间集合管理
class __RoomManager(object):
    managers = {}

    def getRoomSize(self):
        return len(self.managers)

    def getRoomByTag(self, tag):
        room = self.managers.get(tag)
        if room == None:
            room = self.newRoom(self, tag)

        return room

    def newRoom(self, tag):
        room = ClassBean.newRoom(tag)
        self.managers[tag] = room
        return room

    def removeUserById(self, user):
        # print('delete {0}'.format(userId))
        if user is None:
            return
        for room in self.managers.values():
            if user in room.users:
                room.users.remove(user)
                # print('delte later {0}'.format(room.users))
                return


# 唯一 房间管理类

roomManager = __RoomManager()



#连接用户反馈信息
def responseData(user, ws):
    ws.write_message('welcome {0} chessGame ok'.format(user.userName))

#更新房间信息
def updateRoomMsg(room):
    user_count=len(room.users)
    data= model.ResponseData.RoomData.Data(1,1,user_count,4,5,10,123,100,0)
    roomData= model.ResponseData.RoomData(10,1,data)

    msg=json.dumps(roomData,ensure_ascii=False,default=Utils.serialize_instance)
    #便利发送user房间信息
    for user in room.users:
        senRoomMsg2User(msg,user)


#发送信息给user
def senRoomMsg2User(json,user):
    user.userLink.write_message(json)


def joinRoom(user, room1):
    user.go2Room(room1)
    updateRoomMsg(room1)

