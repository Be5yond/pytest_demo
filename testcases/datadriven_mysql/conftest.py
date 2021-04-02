# -*- coding:utf-8 -*-
import allure
import pytest

from utils import db
from lib.lib import LibReq


def pytest_generate_tests(metafunc):
    """
    根据测试类名和方法名加载测试数据
    """
    if 'testdata' in metafunc.fixturenames:
        epic = metafunc.cls.__name__[4:]
        method = metafunc.function.__name__[5:]
        argvalues = db.data_generator(epic, method)

        argnames = ('testdata')
        metafunc.parametrize(argnames, argvalues, scope="function")


@pytest.fixture(scope='class')
def user(request):
    env = request.config.getoption("--env")
    req = LibReq(env=env)
    return req


@allure.step('用户登录')
@pytest.fixture(scope='class')
def user_login(user):
    user.login(data)
    access_token = user.jsan().json.traceId()
    user.acc_token = access_token
    user.cache['acc_token'] = access_token


if __name__ == '__main__':
    pass
