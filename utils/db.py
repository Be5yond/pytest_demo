# -*- coding:utf-8 -*-
import os
import configparser
import redis
import json
# from pymongo import MongoClient
config = configparser.ConfigParser()
HOME_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config.read(HOME_PATH+'/config.ini')
db_cfg = dict(config.items('db'))
redis_cfg = dict(config.items('redis'))


# db_client = MongoClient(db_cfg['host'], int(db_cfg['port']))
# database = db_client.get_database(db_cfg['database'])


# def data_generator(cls, case_id):
#     data = ((i['data'], i['scm']) for i in database[cls][case_id].find({}, {'_id':0}))
#     descs = [i.get('desc', 'No Description') for i in database[cls][case_id].find({}, {'_id':0, 'desc':1})]
#     return data, descs


def get_user_info(key):
    conn = redis.Redis(host=redis_cfg['host'], port=int(redis_cfg['port']), db=int(redis_cfg['database']))
    val = conn.get(key)
    data = json.loads(val.decode())
    return data

