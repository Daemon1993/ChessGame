import os

import tornado.websocket
import tornado.web
import tornado.ioloop

import Presenter


__author__ = 'Daemon1993'
#再试一把,终于能正常通过github客户端提交成年了 我靠!!!!!!!!
class HomeHanlder(tornado.web.RequestHandler):
    def get(self):
        self.render("html/demo.html")

class ChessGameSocket(tornado.websocket.WebSocketHandler):
    def open(self):

        print("WebSocket ip link {0}".format(self.request.remote_ip))
        user = Presenter.userManager.addUser(self,'游客' + str(Presenter.userManager.getUserSize()))

        Presenter.responseData(user, self)

        # 先默认全部进入第一个房间
        room1 = Presenter.roomManager.managers.get('room1')

        Presenter.joinRoom(user,room1)

        count = room1.getUserSize()

        if count >= 2:
            Presenter.disTributePuke(room1)

    def on_message(self, message):

        if message == "createRoom":
            # 获取 房间
            room = Presenter.roomManager.getRoomByTag(Presenter.roomManager, message)
            # puke=ClassManager.getPuke()
            self.write_message('create Room {0} OK users {1}  '.format(room.tag, Presenter.userManager.getUserSize()))
            return

    def on_close(self):
        print("WebSocket closed")

        Presenter.userManager.removeUser(self)

    def check_origin(self, origin):
        return True


def initData():
    return tornado.web.Application([
        ('/soc', ChessGameSocket),
        ('/', HomeHanlder),
    ])


if __name__ == '__main__':
    Presenter.initData(10)
    app = initData()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
