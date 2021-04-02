# -*- coding:utf-8 -*-
import allure
import pytest

from lib.seal import Seal


@pytest.fixture(scope='class')
def user(request):
    """Seal系统实例化一个user

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
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
    user.stash(key='acc_token', json_query='args.traceId')


if __name__ == '__main__':
    pass
