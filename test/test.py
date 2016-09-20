# 单元测试

import Presenter

#前往某个房间
def go2Room():
    user=Presenter.userManager.addUser("id", 'Daemon')

    for index in range(1, 101):
        roomTag="room"+str(index)
        room=Presenter.roomManager.getRoomByTag(Presenter.roomManager,roomTag)
        print('{0} go2Room {1}'.format(user.userName,roomTag))
        isOk=user.go2Room(room)
        if isOk==False:
            print('room {0} Exist user ->{1}'.format(room.tag,user.userName))

    print(user)

#开始给每个用户发扑克
def pukeBegin():
    #print(Presenter.roomManager)
    Presenter.initData()
    print('all room {0} {1}'.format(hex(id(Presenter.roomManager)), len(Presenter.roomManager.managers)))

    room=Presenter.roomManager.managers['room1']

    user1 = Presenter.userManager.addUser("id1", 'Daemon1')
    user2= Presenter.userManager.addUser("id2", 'Daemon2')
    user3 = Presenter.userManager.addUser("id3", 'Daemon3')
    user1.go2Room(room)
    user2.go2Room(room)
    user3.go2Room(room)

    Presenter.disTributePuke(room)

if __name__ == '__main__':
    #go2Room()
    pukeBegin()
