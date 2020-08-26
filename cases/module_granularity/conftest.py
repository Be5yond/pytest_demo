# -*- coding:utf-8 -*-
import allure
import pytest

from lib.seal import Seal
from lib.hippo import Hippo


@pytest.fixture(scope='class')
def user(request):
    """Seal系统实例化一个user

    Returns:
        Session:  a request Session
    """
    env = request.config.getoption("--env")
    ression = Seal(env=env)
    return ression


@pytest.fixture(scope='class')
def auditor(request):
    """Hippo系统实例化一个user

    Returns:
        Session:  a request Session
    """
    env = request.config.getoption("--env")
    ression = Hippo(env=env)
    return ression


@allure.step('seal系统用户登录')
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



@allure.step('hippo 审核员登录')
@pytest.fixture(scope='class')
def auditor_login(auditor):
    data = {
        'username': '{{ user }}',
        'password': '{{ pwd }}'
    }
    auditor.login(data)
    access_token = auditor.jsan().json.password()
    auditor.cache['acc_token'] = access_token


@allure.step('创建一个审核通过的工单')
@pytest.fixture(scope='class')
def create_valid_order(user, auditor):
    user.commit_order()
    order_id = user.jsan().json.type()
    auditor.approve({'order_id': order_id})
    user.cache['order_id'] = order_id

if __name__ == '__main__':
    pass
