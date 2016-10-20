__author__ = 'Daemon1993'

#房间信息
class RoomData:
    def __init__(self,roomType,filed,data):
        self.roomType=roomType
        self.filed=filed
        self.data=data

    class Data:
        def __init__(self,id,blind,number,seatNum,minBuyIn,minOwnerBuyIn,uid,chips,vip=0,img=""):
            self.id=id
            self.blind=blind
            self.number=number
            self.seatNum=seatNum
            self.minBuyIn=minBuyIn
            self.minOwnerBuyIn=minOwnerBuyIn
            self.uid=uid
            self.chips=chips
            self.vip=vip
            self.img=img

class JoinRoom:
    def __init__(self,rid,gameState,status,seatArr):
        self.rid=rid
        self.gameState=gameState
        self.status=status
        self.seatArr=seatArr

    class Seat:
        def __init__(self,uid,pokeArr):
            self.uid=uid
            self.pokerArr=pokeArr

