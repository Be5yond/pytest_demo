
import json
from lib.Req import Req, DefaultData
from consts import urls


class Hippo(Req):
    def __init__(self, env='test'):
        super().__init__(env)
        self._host = self.env_cfg['host']
        self.cache = json.loads(self.env_cfg.get('hippo', '{}'))


    def _get(self, path: str, para: dict):
        """发送get请求

        Args:
            path (str): url path
            para (dict): query parameter

        Returns:
            [Response]: response object
        """
        self.response = self.send('GET', self._host+path, para=para)
        return self.response

    def _post(self, path, data, para=None, header=None):
        """发送post请求

        Args:
            path (str): url path
            para (dict): query parameter
            data (dict): request body 
            header (dict): heder parameter

        Returns:
            [Response]: response object
        """
        para = para or {}
        data = self._update_params(data)
        self.response = self.send('POST', self._host+path, para=para, json=data, header=header)
        return self.response


    def login(self, data):
        """ 登录
        """
        self._post('/post', data)


    def audit(self, order_id: int, is_pass:bool, reject_reason: str = ''):
        """审核工单

        Args:
            order_id (int): 工单id
            is_pass (bool): 是否通过
        """
        pass


    def approve(self, order_id: int):
        """工单审核通过

        Args:
            order_id (int): 工单id
        """
        self.audit(order_id, True)


    def reject(self, order_id: int, reason: str):
        """工单审核驳回

        Args:
            order_id (int): 工单id
            reason (str): 驳回原因
        """
        self.audit(order_id, True, reason)
    

