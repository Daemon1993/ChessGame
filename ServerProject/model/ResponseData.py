__author__ = 'Daemon1993'

#房间信息
class RoomData:
    roomType=None
    filed=None
    data=None
    def __init__(self,roomType,filed,data):
        self.roomType=roomType
        self.filed=filed
        self.data=data

    class Data:
        id =None
        blind=None
        number=None
        seatNum=None
        minBuyIn=None
        minOwnerBuyIn=None
        uid=None
        chips=None
        vip=None
        img=None

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