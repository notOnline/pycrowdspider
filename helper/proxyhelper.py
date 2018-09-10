from threading import Lock
from helper import db
import queue
import threading

status_failed = -1
status_unknown = 0
status_succeed = 4

_queue_proxies_http = queue.Queue()
_queue_proxies_https = queue.Queue()
_abandon_usability = 0
_locker_proxyhelper: Lock = threading.Lock()

_proxies_queues = {}
_abandon_usabilities = {}


def _fetch_proxies(protocol='http'):
    global _proxies_queues
    if protocol not in _proxies_queues:
        _proxies_queues[protocol] = queue.Queue()
        _abandon_usabilities[protocol] = 0
    _queue = _proxies_queues[protocol]
    _abandon_usability = _abandon_usabilities[protocol]

    if _queue.qsize() < 2000:
        _queue.queue.clear()
        all_proxies = db.proxies.find({'protocol': protocol}).sort([('usability', -1)]).limit(10000)
        for proxy in all_proxies:
            _queue.put(proxy)
            _abandon_usability = min(_abandon_usability, proxy['usability'])
    return _queue


def next(protocol, thread_id=-1):
    global _locker_proxyhelper
    # print('next_thread_id[{}].acquire->_locker_proxyhelper'.format(thread_id))
    if _locker_proxyhelper.acquire():
        proxy = _fetch_proxies(protocol).get_nowait()
        # print('next_thread_id[{}].release->_locker_proxyhelper'.format(thread_id))
    _locker_proxyhelper.release()
    print(proxy)
    return proxy


def reback(proxy, status, thread_id):
    global _locker_proxyhelper
    # print('reback_thread_id[{}].acquire->_locker_proxyhelper'.format(thread_id))
    if _locker_proxyhelper.acquire():

        proxy['usability'] += status
        db.proxies.update_one({'_id': proxy['_id']}, {"$set": {'usability': proxy['usability']}})
        if proxy['usability'] >= _abandon_usability:
            _proxies_queues[proxy['protocol']].put(proxy)
        # print('reback_thread_id[{}].release->_locker_proxyhelper'.format(thread_id))
        _locker_proxyhelper.release()


'''
def get_nowait():
    if queue_proxies.qsize() < 500:
        _fetch_proxies()
    return queue_proxies.get_nowait();


def put(proxy, status):
    proxy['usability'] += status
    db.update_one('proxies', {'_id': proxy['_id']}, {'usability': proxy['usability']})
    if proxy['usability'] >= abandon_usable_value:
        queue_proxies.put(proxy)
'''
