import random

import json
import logging
import ActionProtocol

logger = logging.getLogger(__name__)

#aaaaa
def getRandomPuke(pukes):

    puke=random.choice(pukes)

    pukes.remove(puke)
    return puke



#生成json 传给客户端
def parseSendJson(obj):
    msg = json.dumps(obj, ensure_ascii=False, default=serialize_instance)
    return msg


def serialize_instance(obj):
    d = {}
    d.update(vars(obj))
    return d
