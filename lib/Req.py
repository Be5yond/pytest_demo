
import re
from json import JSONDecodeError
import jsane
import pytest
import requests
from schema import Schema, SchemaError

from comm.logger import logger
from comm.render import render


class Req(object):
    def __init__(self):
        self.session = requests.Session()
        self.response = None
        self.cache = {}

    def send(self, method, url, variable=None, para=None, json=None, data=None, header=None, files=None):
        """
        send request.
        Params:
        | method | request method | # POST |
        | url | target url |
        | variable | kwargs in url |
        | params | kwargs for get method |
        | data | kwargs in request body form format|
        | headers | custom header |
        | files | # TBD |
        :return: response
        """

        if variable:
            for key, value in variable.items():
                url = url.replace(key, str(value))
        req = requests.Request(method, url, params=para, json=json, data=data, headers=header, files=files)
        prepped = self.session.prepare_request(req)
        self.response = self.session.send(prepped)

        logger.debug('<= request url => \n{}'.format(self.response.request.url))
        body = json or data
        logger.debug('<= request data => \n{}'.format(jsane.dumps(body, indent=4, ensure_ascii=False)))
        logger.debug('<= response data => \n{}'.format(jsane.dumps(self.jsan().r(), indent=4, ensure_ascii=False)))

        return self.response

    def validate_resp(self, scm):
        """

        :param scm: schema data
        :return:
        """
        data = self.response.json()
        scm = self._update_params(scm)
        schema = Schema(scm, ignore_extra_keys=True)
        try:
            schema.validate(data)
            logger.debug('<= schema template => \n{}'.format(scm))
        except SchemaError as e:
            logger.error('<= schema template => \n{}'.format(scm))
            logger.error('<= err msg => \n{}'.format(e))
            pytest.fail(msg=str(e), pytrace=False)

    def jsan(self):
        """
        :return: response jsane traversable object
        """

        try:
            return jsane.from_dict(self.response.json())
        except JSONDecodeError as e:
            logger.debug('<= err msg => \n{}'.format(e))
            logger.debug('<= response content => \n{}'.format(self.response.content))
            pytest.fail('response data format does not match the JSON format')

    def _update_params(self, para):
        return render(para, self.cache)



if __name__=='__main__':
    req = Req()
    req.cache.update({'val': 419})
    a={'key':'{% str %}', 'key_lst':[{'lk':'{% int %}'},'uiui', 9090],'key_dict': {'dk': 7879, 'dk2':'{% True %}'}}
    print(req._update_params(a))
    import time
    start = time.time()
    for _ in range(1):
        b = {
            'key': {
                'lk': '{% fake.pystr(max_chars=10) %}',
                'phone': '{% fake.phone_number() %}',
                'company': '{% fake.company() %}',
                'str': '{% str %}',
                'tu':['{{ val }}', {'newkey': '{{ val }}'}]
            }
        }
        print(req._update_params(b))
    print(time.time()- start)

