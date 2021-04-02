import allure
import json

class TestUserClass(object):
    @allure.feature("用户登陆")
    def test_user_login_pass(self, user, data):
        with allure.step(data.title):
            user.login(data.step)
            user.validate(data.schema)

    @allure.feature("用户登陆")
    def test_user_login_fail(self, user, data):
        with allure.step(data.title):
            user.login(data.step)
            user.validate(data.schema)
