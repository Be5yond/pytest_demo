import time
import random
import string


def get_current_time_str():
    return time.strftime('%Y%m%d%H%M%S', time.localtime())


def randstr(l):
    """
    :param l: string length
    :return: a string object
    """
    return ''.join((random.choice(string.ascii_letters) for i in range(l)))
