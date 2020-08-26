from cases.module_granularity.conftest import auditor
import pytest
import allure


@pytest.mark.usefixtures("user_login", "auditor_login")
class TestAuditClass(object):
    @allure.feature("工单审核")
    @pytest.mark.parametrize('data,scm', [
        ([
            {'type': 1, 'category': 'category'}, 
            {'result': 1, 'reason': ''}, 
            {'order_id': '{{ order_id }}'}
         ], 
         {
            'args': '{% dict %}'
         }),
    ])
    def test_audit_pass(self, user, auditor, data, scm):
        with allure.step('提交工单'):
            user.commit_order(data[0])
            user.cache['order_id'] = user.jsan().json.type()
        with allure.step('审核通过'):
            auditor.approve(data[1])
        with allure.step('查看工单状态'):
            user.get_order_detail(data[2])
            user.validate_resp(scm)
