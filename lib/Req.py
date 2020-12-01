import re
import os
import json
import jsane
import jmespath
import pytest
import configparser
import requests
from copy import copy
from schema import Schema, SchemaError

from comm.logger import logger
from comm.render import render


class Req(object):
    def __init__(self, env='test'):
        self.session = requests.Session()
        self.response = None
        config = configparser.ConfigParser()
        HOME_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config.read(HOME_PATH + '/config.ini')
        self.env_cfg = dict(config.items('env_{}'.format(env)))
        self.cache = json.loads(self.env_cfg.get('cache', '{}'))

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
            url = url.format(**variable)
        req = requests.Request(method, url, params=para, json=json, data=data, headers=header, files=files)
        prepped = self.session.prepare_request(req)
        self.response = self.session.send(prepped)

        logger.debug('<= request url => \n{}'.format(self.response.request.url))
        body = json or data
        logger.debug('<= request data => \n{}'.format(jsane.dumps(body, indent=4, ensure_ascii=False)))
        logger.debug('<= response data => \n{}'.format(jsane.dumps(self.jsan().r(), indent=4, ensure_ascii=False)))
        logger.debug('<= time elapsed => \n{}s'.format(self.response.elapsed.total_seconds()))
        return self.response

    def validate_resp(self, scm: str):
        """ 校验response返回数据

        Args:
            scm (str): 数据校验模板
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
        
    def validate_data(self, json_query: str, scm: str):
        """ 校验返回体的部分字段

        Args:
            json_query (str): 待校验数据的json_query,
            scm (str): 数据校验模板
        """
        data = jmespath.search(json_query, self.response.json())
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
        except json.JSONDecodeError as e:
            logger.debug('<= err msg => \n{}'.format(e))
            logger.debug('<= response content => \n{}'.format(self.response.content))
            pytest.fail('response data format does not match the JSON format')

    def stash(self, path: str, key: str):
        """ 通过path取出数据并，缓存数据到cache

        Args:
            path (str): jsonpath for target object
            key (str): data key in self.cache 
        """
        self.cache[key] = jmespath.search(path, self.response.json())

    def _update_params(self, para: object) -> object:
        return render(para, self.cache)



class DefaultData:
    def __init__(self, **kwargs):
        self.temp = kwargs

    def __call__(self, func):
        def wrap(*args, **kwargs):
            for k, v in self.temp.items():
                temp = copy(v)
                temp.update(kwargs.get(k, {}))
                kwargs[k] = temp
            return func(*args, **kwargs)
        return wrap


if __name__ == '__main__':
    req=Req()

