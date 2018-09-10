import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

_client: MongoClient = pymongo.MongoClient(host='localhost', port=27017)
_db_spider: Database = _client.get_database('py_crowd_spider')
jobs: Collection = _db_spider['spider_job']
raw_data: Collection = _db_spider['raw_data']
proxies: Collection = _db_spider['proxies']

douban_tags: Collection = _db_spider['douban_tag']
book_briefs: Collection = _db_spider['book_briefs']
book_details: Collection = _db_spider['book_details']
'''
_db_douban: Database = _client.get_database('douban')
douban_raw_data: Collection = _db_douban['raw_data']


def add_one(table, model):
    return db[table].insert_one(model).inserted_id


def add_job_one(job):
    if not get_one('spider_job', {'url': job['url']}):
        add_one("spider_job", job)


def add_many(table, models):
    return db[table].insert_many(models).inserted_ids


def get_one(table, condition):
    return db[table].find_one(condition)


def get_all(table, sort={'_id': 1}, limit=10000000):
    __sort = []
    for key in sort:
        __sort.append((key, sort[key]))
    return db[table].find().sort(__sort).limit(limit)


def update_one(table, model, post):
    db[table].update_one(model, {"$set": post}, upsert=False)


def delete_one(table, condition):
    db[table].find_one_and_delete(condition)
'''
