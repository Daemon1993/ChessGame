
from model import ClassBean
import ActionProtocol,Utils
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

__author__ = 'Daemon1993'

'''
主持人 逻辑控制者
'''


def initData(size):

    # 初始化 房间数
    for index in range(1, size+1):
        roomTag = "room" + str(index)
        roomManager.newRoom(roomTag)

    logger.info('all room {0}'.format(len(roomManager.managers)))


    #客户端的回调 功能添加
    ActionProtocol.initActionsFromC()

    # ActionFromClient.action_dicts[1]=action1
    # print(ActionFromClient.action_dicts)


# 开始 puke
def disTributePuke(room):
    win_user = room.showPuke()
    if win_user is not None:
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
            logger.warning('用户已经存在')
        else:
            user = ClassBean.newUser(userLink, userName)

        self.users[userLink] = user

        return user

    def getUserSize(self):
        return len(self.users)

    # 用户下线
    def removeUser(self, userLink):

        user=self.users[userLink]
        logger.info("掉线 {0}".format(user))

        # 删除当前账号的房间的当前用户

        roomManager.removeUser(user)

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

    def removeUser(self, user):
        # print('delete {0}'.format(userId))
        if user is None:
            return
        for room in self.managers.values():
             if user in room.users:
                user.exitRoom(room)
                #print('delte later {0}'.format(room.users))
                break
                # return


# 唯一 房间管理类

roomManager = __RoomManager()



#连接用户反馈信息
def responseData(user, ws):
    ws.write_message('welcome {0} chessGame ok'.format(user.userName))

#更新房间信息
def updateRoomMsg(room):
    room.updateRoom()


def joinRoom(user, room1):
    user.go2Room(room1)
    updateRoomMsg(room1)



def parseAction(user_link,message):
    Utils.parseAction(user_link, message, ActionProtocol.action_dicts_from_c)
