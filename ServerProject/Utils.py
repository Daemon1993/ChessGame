import random

import ServerProject.model.ResponseData

#aaaaa
def getRandomPuke(pukes):
    size=len(pukes)
    index=random.randint(0,size)

    puke=pukes[index]
    pukes.remove(puke)
    return puke

def serialize_instance(obj):
    d = {}
    d.update(vars(obj))
    return d


classes = {
    'RoomData' : ServerProject.model.ResponseData.RoomData
}

def unserialize_object(d):
    clsname = d.pop('__classname__', None)
    if clsname:
        cls = classes[clsname]
        obj = cls.__new__(cls) # Make instance without calling __init__
        for key, value in d.items():
            setattr(obj, key, value)
        return obj
    else:
        return d
