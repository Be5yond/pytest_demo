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


def pytest_configure(config):
    env = config.getoption('env')
    for item in db.config.items('env_{}'.format(env)):
        config.cache.set(*item)


def pytest_runtest_setup(item):
    pass


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test",
        help="environment: test or online")


def pytest_collectstart(collector):
    pass


def clean_env():
    print('=========================')


@pytest.fixture(scope='class')
def user(request):
    request.addfinalizer(clean_env)
    host = request.config.cache.get('host', None)
    req = LibReq(host=host)
    req.source = 'shopmall'
    req.cache['user'] = request.config.cache.get('user', None)
    req.cache['pwd'] = request.config.cache.get('pwd', None)
    return req


@allure.step('用户登录')
@pytest.fixture(scope='class')
def user_login(user):
    data = {
        "username": "{{ user }}",
        "password": "{{ pwd }}",
    }
    user.login(data)
    access_token = user.jsan().json.traceId()
    user.acc_token = access_token
    user.cache['acc_token'] = access_token


if __name__ == '__main__':
    pass
