# -*- coding:utf-8 -*-
import allure
import pytest

from comm import db
from lib.lib import LibReq


def pytest_generate_tests(metafunc):
    if 'data' in metafunc.fixturenames:
        argnames = ('data', 'scm')
        argvalues, ids = db.data_generator(metafunc.cls.__name__, metafunc.function.__name__)
        metafunc.parametrize(argnames, argvalues, ids=ids,scope="function")


@pytest.fixture(scope='class')
def user(request):
    env = request.config.getoption("--env")
    req = User(env=env)
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
