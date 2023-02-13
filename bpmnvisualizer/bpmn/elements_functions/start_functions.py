import random as r
# import numpy as np

def sequence(*seq):
    def toRet(time):
        return seq[time % len(seq)]
    return toRet


def random(n1, n2):
    def toRet(time):
        return r.randint(n1, n2)
    return toRet


def puasson():
    def toRet(time):
        return r.randint(0, 2)
    return toRet

#def normal(mu, sigma):
#    def toRet(time):
#        return int(np.random.normal(mu, sigma))
#    return toRet

