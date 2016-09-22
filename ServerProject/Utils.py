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
