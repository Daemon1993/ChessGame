import random

import ServerProject.model.ResponseData

#aaaaa
def getRandomPuke(pukes):

    puke=random.choice(pukes)

    pukes.remove(puke)
    return puke

