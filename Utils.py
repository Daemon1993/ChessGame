
import random
#aaaaa
def getRandomPuke(pukes):
    index=random.randint(0,51)
    puke=pukes[index]
    pukes.remove(puke)
    return puke
