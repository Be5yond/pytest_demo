import pytest
import allure


class TestUserClass(object):

    @allure.feature("用户登陆")
    def test_user_login_pass(self, user, data, scm):
        with pytest.allure.step('login'):
            user.login(data)
            user.validate_resp(scm)


@pytest.mark.usefixtures("user_login")
class TestProductClass(object):
    @allure.feature("商品查询")
    def test_product_detail_get(self, user, data, scm):
        with pytest.allure.step('login'):
            user.login(data)
            user.validate_resp(scm)
