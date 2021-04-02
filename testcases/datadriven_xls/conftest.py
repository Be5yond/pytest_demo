# -*- coding:utf-8 -*-
import allure
import pytest

from comm.xls import gen_data
from lib.lib import LibReq


def idfn(val):
    return val.get('type', 'wide')


def pytest_generate_tests(metafunc):
    if 'data' in metafunc.fixturenames:
        argnames = 'data'
        argvalues = gen_data(metafunc.cls.__name__, metafunc.function.__name__)
        metafunc.parametrize(argnames, argvalues, ids=idfn, scope="function")


@pytest.fixture(scope='class')
def user(request):
    env = request.config.getoption("--env")
    req = LibReq(env=env)
    return req


@allure.step('用户登录')
@pytest.fixture(scope='class')
def user_login(user):
    data = {
        'username': '{{ user }}',
        'password': '{{ pwd }}'
    }
    user.login(data)
    access_token = user.jsan().json.traceId()
    user.acc_token = access_token
    user.cache['acc_token'] = access_token
