import uuid
import time
from lib.Req import Req, DefaultData


class LibReq(Req):
    def __init__(self, env='test'):
        super().__init__(env)
        self._host = self.env_cfg['host']

    def _get(self, path, para):
        """
        send get request
        Params:
        | params | query args dict |
        Return: response object
        """
        params = self._add_common_params(para)

        self.response = self.send('GET', self._host+path, para=para)
        return self.response

    def _post(self, path, data, para=None, header=None):
        """
        send post request
        Params:
        | data | body args dict |
        Return: response object
        """
        para = para or {}
        data = self._update_params(data)
        data = self._add_common_params(data)
        self.response = self.send('POST', self._host+path, para=para, json=data, header=header)
        return self.response

    def _add_common_params(self, args):
        trace_id = str(uuid.uuid4())
        self.cache['trace_id'] = trace_id
        args.update({'traceId': trace_id,
                     'timestamp': int(time.time()*1000),
                    })
        return args

    def login(self, data):
        self._post('/post', data)

    @DefaultData(data={
        "StartTime": "{% timestr(minutes=-65) %}",
        "EndTime": "{% timestr() %}",
        "Type": "default"
    })
    def get_pv(self, para):
        self._get('/get', para)


