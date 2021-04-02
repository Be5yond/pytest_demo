import pytest
import allure
import json


class TestUserClass(object):
    @allure.feature("用户登陆")
    def test_user_login_pass(self, user, data):
        with pytest.allure.step(data['id']):
            data.pop('id')
            scm = json.loads(data.pop('scm'))

        with pytest.allure.step('login'):
            user.login(data)
            user.validate_resp(scm)

    @allure.feature("用户登陆")
    def test_user_login_fail(self, user, data):
        with pytest.allure.step(data['id']):
            data.pop('id')
            scm = json.loads(data.pop('scm'))

        with pytest.allure.step('login'):
            user.login(data)
            user.validate_resp(scm)
