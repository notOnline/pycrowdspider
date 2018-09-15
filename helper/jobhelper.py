from threading import Lock
from helper import db
import queue
import threading

status_failed = -1
status_init = -100
status_succeed = 1

_queue_jobs = queue.Queue()
_locker_jobhelper: Lock = threading.Lock()


def _fetch_jobs():
    global _queue_jobs
    if _queue_jobs.empty():
        _all = db.jobs.find({'status': status_init}).limit(500)
        for _one in _all:
            _queue_jobs.put(_one)


def next():
    global _locker_jobhelper
    with _locker_jobhelper:
        _fetch_jobs()
        job = None
        if not _queue_jobs.empty():
            job = _queue_jobs.get_nowait()
        return job


def complete(job, status):
    global _locker_jobhelper
    with _locker_jobhelper:
        db.jobs.update_one({'_id': job['_id']}, {"$set": {'status': status}})
