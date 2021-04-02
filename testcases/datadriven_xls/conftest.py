# -*- coding:utf-8 -*-
import allure
import pytest

from utils.xls import gen_data
from lib.seal import Seal


def idfn(val):
    return val.get('id', 'wide')


def pytest_generate_tests(metafunc):
    if 'data' in metafunc.fixturenames:
        argnames = 'data'
        argvalues = gen_data(metafunc.cls.__name__, metafunc.function.__name__)
        metafunc.parametrize(argnames, argvalues, scope="function")


@pytest.fixture(scope='class')
def user(request):
    env = request.config.getoption("--env")
    req = Seal(env=env)
    return req


@allure.step('用户登录')
@pytest.fixture(scope='class')
def user_login(user):
    data = {
        'username': '{{ user }}',
        'password': '{{ pwd }}'
    }
    user.login(data)
