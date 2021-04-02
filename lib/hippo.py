
import json
from testtp import Session, defaultdata
from consts import urls
from utils import config


class Hippo(Session):
    def __init__(self, env='test'):
        super().__init__()
        self.config = config.config[f'env_{env}']
        self._host = self.config['hippo_host']
        self.cache = json.loads(self.config['hippo_cache'])


    def login(self, data):
        """ 登录
        """
        return self.post(self._host+urls.LOGIN_HIPPO, json=data)


    def audit(self, **kwargs):
        """审核工单
        """
        return self.post(self._host+urls.ORDER_AUDIT, **kwargs)


    def approve(self, order_id: int):
        """工单审核通过

        Args:
            order_id (int): 工单id
        """
        data = {
            'order_id': order_id,
            'pass': True
        }
        self.audit(json=data)


    def reject(self, order_id: int, reason: str):
        """工单审核驳回

        Args:
            order_id (int): 工单id
            reason (str): 驳回原因
        """
        data = {
            'order_id': order_id,
            'reason': reason,
            'pass': False
        }
        self.audit(json=data)
    

