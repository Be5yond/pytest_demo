import time
import random
import string
import arrow


def get_current_time_str():
    return time.strftime('%Y%m%d%H%M%S', time.localtime())


def randstr(l):
    """
    :param l: string length
    :return: a string object
    """
    return ''.join((random.choice(string.ascii_letters) for i in range(l)))


def timestr(**kwargs):
    """
    generate "2017-03-07T00:00+0800" format time string
    :param kwargs: shifting parameters e.g. hours=3  days=-1
    :return:
    """
    now = arrow.now(tz='Asia/Shanghai')
    t = now.shift(**kwargs)
    return t.format('YYYY-MM-DDTHH:mm+0800')
