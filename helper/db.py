import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import config

_client: MongoClient = pymongo.MongoClient(host=config.mongodb_host, port=config.mongodb_port)

_db_spider: Database = _client.get_database('py_crowd_spider')
jobs: Collection = _db_spider['spider_job']
raw_data: Collection = _db_spider['raw_data']
book_details: Collection = _db_spider['book_details']

_db_douban: Database = _client.get_database('douban')
book_tags=_db_douban['book_tags']
book_briefs: Collection = _db_douban['book_briefs']
new_book_details: Collection = _db_douban['book_details']
new_book_details_1:  Collection = _db_douban['book_details_1']

_db_proxies: Database = _client.get_database('proxies')
proxies: Collection = _db_proxies['proxies']
