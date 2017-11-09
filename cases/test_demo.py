import pytest
import allure


class TestUserClass(object):

    @allure.feature("用户登陆")
    def test_user_login_pass(self, user):
        with pytest.allure.step('login'):
            data = {
                "username": "{{ user }}",
                "password": "{{ pwd }}",
            }
            scm = {'json': data}
            user.login(data)
            user.validate_resp(scm)


@pytest.mark.usefixtures("user_login")
class TestProductClass(object):
    @allure.feature("商品查询")
    def test_product_detail_get(self, user):
        with pytest.allure.step('login'):
            data = {
                "username": "{{ user }}",
                "password": "{{ pwd }}",
            }
            scm = {'json': data}
            user.login(data)
            user.validate_resp(scm)
