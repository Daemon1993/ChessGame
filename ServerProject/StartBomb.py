import os
import urllib

import pymongo
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define,options
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import Presenter

__author__ = 'Daemon1993'


define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")


# 再试一把,终于能正常通过github客户端提交成年了 我靠!!!!!
class HomeHanlder(tornado.web.StaticFileHandler):
    pass


# 获取协议 接口
class GetProtocolHanlder(tornado.web.RequestHandler):
    def get(self):
        self.write('给你协议的接口')



class ChessGameSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        logger.debug("WebSocket ip link {0}".format(self.request.remote_ip))
        user = Presenter.userManager.addUser(self, '游客' + str(Presenter.userManager.getUserSize()))

        Presenter.responseData(user, self)
        # 先默认全部进入第一个房间
        room1 = Presenter.roomManager.managers.get('room1')
        Presenter.joinRoom(user, room1)
        count = room1.getUserSize()

        if count >= 2:
            Presenter.disTributePuke(room1)

    def on_message(self, message):
        Presenter.parseAction(self, message)

        # if message == "createRoom":
        #     # 获取 房间
        #     room = Presenter.roomManager.getRoomByTag(Presenter.roomManager, message)
        #     # puke=ClassManager.getPuke()
        #     self.write_message('create Room {0} OK users {1}  '.format(room.tag, Presenter.userManager.getUserSize()))
        #     return

    def on_close(self):
        logger.info("WebSocket closed")

        Presenter.userManager.removeUser(self)

    def check_origin(self, origin):
        return True
        # parsed_origin = urllib.parse.urlparse(origin)

        # return parsed_origin.netloc.endswith(".huoor.com")



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/demo.html")


def initData():
    return tornado.web.Application(
        [
        ('/main', ChessGameSocket),
        ('/getProtocol', GetProtocolHanlder),
        ("/index", IndexHandler),
        ],
    )


if __name__ == '__main__':
    logger.info('Bmob start.......')

    user={"_id":'daemon'}

    conn = pymongo.MongoClient(host='112.74.207.72', port=27017)
    print(conn.address)
    db_auth = conn.admin
    db_auth.authenticate('daemon', 'daemon123')
    # collection = db_auth.ajinomoto_menu
    collection = db_auth.GUser
    try:
        collection.insert(user)
    except Exception as e:
        logger.info('user name {0} has exist'.format(user['_id']))

    Presenter.initData(10)
    app = initData()


    app.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()


