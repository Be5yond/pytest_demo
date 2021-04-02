import pytest
import allure


class TestUserClass(object):
    @allure.feature("用户登陆")
    @pytest.mark.parametrize('data,scm', [
        ({}, {'data': '{% str %}'}),
    ])
    def test_user_login_pass(self, user, data, scm):
        with allure.step('login'):
            user.login(data)
            user.validate(scm)

    @allure.feature("用户登陆")
    @pytest.mark.parametrize('data,scm', [
        ({'username': '{{ user }}', 'password': 'wrong'}, {'data': '{% str %}'}),
        ({'username': 'wrong', 'password': '{{ pwd }}'}, {'data': '{% str %}'})
    ])
    def test_user_login_fail(self, user, data, scm):
        with allure.step('login'):
            user.login(data)
            user.validate(scm)


@pytest.mark.usefixtures("user_login")
class TestProductClass(object):
    @allure.feature("商品查询")
    @pytest.mark.parametrize('data,scm', [
        ({'type': 1, 'category': 'category'}, {'data': '{% str %}'}),
    ])
    def test_product_detail_get(self, user, data, scm):
        with allure.step('login'):
            user.login(data)
            user.validate(scm)


@pytest.mark.usefixtures("user_login")
class TestProductClass(object):
    @allure.feature("商品查询")
    @pytest.mark.parametrize('data,scm', [
        ({'type': 1, 'category': 'category'}, {'data': '{% str %}'}),
    ])
    def test_product_detail_get(self, user, data, scm):
        with allure.step('login'):
            user.login(data)
            user.validate(scm)
