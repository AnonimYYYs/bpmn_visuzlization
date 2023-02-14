import random as r


def constant(n):
    def toRet():
        return int(n)
    return toRet


def random(n1, n2):
    def toRet():
        return r.randint(int(n1), int(n2))
    return toRet


def lin_res(res_low, res_high, time_low, time_high, curr_res):
    def toRet():
        m = (int(time_low) - int(time_high)) / (int(res_low) - int(res_high))
        return round(m * (int(curr_res) - int(res_high)) + int(time_high))
    return toRet


