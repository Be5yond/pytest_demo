# -*- coding:utf-8 -*-
import allure
import pytest

from comm import db
from lib.lib import LibReq


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


if __name__ == '__main__':
    pass
