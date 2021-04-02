
import uuid
import time
import json

from testtp import Session, defaultdata
from consts import urls
from utils import config


class Seal(Session):
    def __init__(self, env='test'):
        super().__init__()
        self.config = config.config[f'env_{env}']
        self._host = self.config['seal_host']
        self.cache = json.loads(self.config['seal_cache'])
        self.params = self._common_params()

    def _common_params(self):
        trace_id = str(uuid.uuid4())
        # self.cache['trace_id'] = trace_id
        args = {
            'traceId': trace_id,
            'timestamp': int(time.time()*1000),
            }
        return args

    def login(self, data: dict):
        """登录

        Args:
            data (dict): 请求参数
        """
        self.post(self._host+urls.LOGIN_SEAL, json=data)

    @defaultdata(params={
        "StartTime": "{% timestr(minutes=-65) %}",
        "EndTime": "{% timestr() %}",
        "Type": "default"
    })
    def query_stats(self, **kwargs):
        self.post(self._host+urls.QEURY_STATS, **kwargs)

    def commit_order(self, data: dict):
        """提交工单

        Args:
            data (dict): 工单信息
        """
        self.post(self._host+urls.ORDER_COMMIT, data)

    def get_order_detail(self, data: dict):
        """提交工单

        Args:
            data (dict): 工单信息
        """
        self.get(self._host+urls.ORDER_DETAIL, data)
        

