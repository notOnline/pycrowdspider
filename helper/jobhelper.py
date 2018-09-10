from threading import Lock
from helper import db
import queue
import threading

status_failed = -1
status_init = -100  # 0
status_succeed = 1

_queue_jobs = queue.Queue()
_locker_jobhelper: Lock = threading.Lock()


def _fetch_jobs():
    global _queue_jobs
    if _queue_jobs.empty():
        _queue_jobs.queue.clear()
        _all = db.jobs.find({'status': status_init}).limit(500)
        for _one in _all:
            _queue_jobs.put(_one)


def next(thread_id):
    global _locker_jobhelper
    # print('thread_id[{}].acquire->_locker_jobhelper'.format(thread_id))
    if _locker_jobhelper.acquire():
        _fetch_jobs()
        job = None
        if not _queue_jobs.empty():
            job = _queue_jobs.get_nowait()
        # print('thread_id[{}].release->_locker_jobhelper'.format(thread_id))
        _locker_jobhelper.release()
    return job


def complete(job, status, thread_id):
    global _locker_jobhelper
    # print('thread_id[{}].acquire->_locker_jobhelper'.format(thread_id))
    if _locker_jobhelper.acquire():
        db.jobs.update_one({'_id': job['_id']}, {"$set": {'status': status}})
        # print('thread_id[{}].release->_locker_jobhelper'.format(thread_id))
        _locker_jobhelper.release()
