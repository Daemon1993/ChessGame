import tornado.ioloop
import tornado.web
import tornado.websocket
import os

from ServerProject import Presenter,DataParse

__author__ = 'Daemon1993'
#再试一把,终于能正常通过github客户端提交成年了 我靠!!!!!
class HomeHanlder(tornado.web.StaticFileHandler):
    pass

#获取协议 接口
class GetProtocolHanlder(tornado.web.RequestHandler):
    def get(self):

        self.write('给你协议')

class ChessGameSocket(tornado.websocket.WebSocketHandler):
    def open(self):

        print("WebSocket ip link {0}".format(self.request.remote_ip))
        user = Presenter.userManager.addUser(self, '游客' + str(Presenter.userManager.getUserSize()))

        Presenter.responseData(user, self)
        # 先默认全部进入第一个房间
        room1 = Presenter.roomManager.managers.get('room1')
        Presenter.joinRoom(user, room1)
        count = room1.getUserSize()

        if count >= 2:
            Presenter.disTributePuke(room1)

    def on_message(self, message):

        DataParse.parseAction(message)

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

class IndexHandler(tornado.web.RequestHandler):

    def get(self):

        self.render("static/demo.html")




class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("GameHall/build/web-desktop/index.html")




def initData():
    return tornado.web.Application([
        ('/main', ChessGameSocket),
        ('/getProtocol', GetProtocolHanlder),
        ("/zjb", HomeHandler),
        ("/index", IndexHandler),

    ])


def beginBmob():
    print(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

    Presenter.initData(10)
    app = initData()

    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

