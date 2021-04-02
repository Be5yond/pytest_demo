# -*- coding:utf-8 -*-
import redis
import json
import pytest
# from pymongo import MongoClient
from peewee import MySQLDatabase, Model
from peewee import CharField, PrimaryKeyField, TextField, IntegerField

from . import config

testdata_db_cfg = config.config('db')
redis_cfg = dict(config.items('redis'))

# db_client = MongoClient(db_cfg['host'], int(db_cfg['port']))
# database = db_client.get_database(db_cfg['database'])


class TestData(Model):
    id = PrimaryKeyField()
    title = CharField()
    description = CharField()
    epic = CharField()
    method = CharField()
    precondition = TextField()
    step = TextField()
    extract = TextField()
    schema = TextField()

    class Meta:
        database = MySQLDatabase(testdata_db_cfg['db'],
                                 user=testdata_db_cfg['username'],
                                 password=testdata_db_cfg['password'],
                                 host=testdata_db_cfg['host'],
                                 port=3306)
        table_name = 'tb_testdata'

    def loads(self):
        default = '[]'
        try:
            self.precondition = json.loads(self.precondition or default)
            self.step = json.loads(self.step or default)
            self.schema = json.loads(self.schema or default)
            self.extract = json.loads(self.extract or default)
        except json.JSONDecodeError as e:
            pytest.fail('------load testdata failed ------ : \n', e)
        return self


def get_user_info(key):
    conn = redis.Redis(host=redis_cfg['host'],
                       port=int(redis_cfg['port']),
                       db=int(redis_cfg['database']))
    val = conn.get(key)
    data = json.loads(val.decode())
    return data
