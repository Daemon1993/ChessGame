import random


#aaaaa
def getRandomPuke(pukes):

    puke=random.choice(pukes)

    pukes.remove(puke)
    return puke

