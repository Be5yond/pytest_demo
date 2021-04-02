import configparser
import json
import pytest
from json import JSONDecodeError
# from MySQLdb import _mysql
from peewee import MySQLDatabase, Model 
from peewee import CharField, PrimaryKeyField, TextField, IntegerField
from .import config

db_cfg = dict(config.items('db'))


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
        database = MySQLDatabase(db_cfg['db'], user=db_cfg['username'], password=db_cfg['password'], host=db_cfg['host'], port=3306)
        table_name = 'tb_testdata'
    def loads(self):
        default = '[]'
        try:
            self.precondition = json.loads(self.precondition or default)
            self.step = json.loads(self.step or default)
            self.schema = json.loads(self.schema or default)
            self.extract = json.loads(self.extract or default)
        except JSONDecodeError as e:
            pytest.fail('------load testdata failed ------ : \n', e)
        return self

def data_generator(cls, method):
    ret = TestData.select().where(TestData.epic == cls, TestData.method == method)
    ret = [d.loads() for d in ret]
    return ret