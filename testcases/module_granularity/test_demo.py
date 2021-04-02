import pytest
import allure


@pytest.mark.usefixtures("user_login", "auditor_login")
class TestAuditClass(object):
    @allure.feature("工单审核")
    @pytest.mark.parametrize('data,scm', [
        (
            [
                {'type': 1, 'category': 'category'}, 
                {'result': 1, 'reason': ''}, 
                {'order_id': '{{ order_id }}'}
            ],   #  data数据
            {'args': '{% dict %}'}  # schema数据
        ),  # 第一组数据
        (
            [
                {'type': 2, 'category': 'category'}, 
                {'result': 1, 'reason': ''}, 
                {'order_id': '{{ order_id }}'}
            ],   # data数据
            {'args': '{% dict %}'} # schema数据
        ),  #第二组数据
    ])
    def test_audit_pass(self, user, auditor, data, scm):
        with allure.step('1.提交工单'):
            user.commit_order(data[0])
            user.stash('json.type', 'order_id')
        with allure.step('2.审核通过'):
            auditor.approve(data[1])
        with allure.step('3.验证工单状态为已通过'):
            user.get_order_detail(data[2])
            user.validate(scm)

    @allure.feature("工单审核")
    @pytest.mark.parametrize('data,scm', [
        ({'order_id': '{{ order_id }}'}, {'args': '{% dict %}'})
    ])
    def test_order_detail(self, create_valid_order, user, data, scm):
        user.get_order_detail(data)
        user.validate(scm)

