# coding:utf-8
import threading
from threading import Lock

from downloader import downloader
from helper import db, loghelper, filehelper, jobhelper

_locker_proxyhelper: Lock = threading.Lock()
_job_status_init = 0
_job_status_crawling = 2
_job_status_succeed = 1
_job_status_failed = -1


def execute(thread_id):
    loghelper.info('start:excute({})'.format(thread_id))
    job = jobhelper.next(thread_id)
    while job is not None:
        # print('-------------------thread_id:{}--------------'.format(thread_id))
        url = job['url']
        loghelper.info('start:' + url, thread_id)
        model = db.raw_data.find_one({'url': url})
        if model:
            html = open(model['html_file_path'], 'r', encoding='utf-8').read()
        else:
            html = downloader.download(url, auto_protocol=job['auto_protocol'], thread_id=thread_id)
        html_file_path = filehelper.write(html)
        db.raw_data.insert_one({'url': url, 'html_file_path': html_file_path})
        extractor = __import__('extractor', globals(), locals(), [job['extractor']])
        real_extractor = eval('extractor.' + job['extractor'])
        try:
            real_extractor.extract(html=html, job_args=job['job_args'], url=url)
        except Exception as msg:
            loghelper.error(msg)
            jobhelper.complete(job, jobhelper.status_failed, thread_id=thread_id)
        else:
            jobhelper.complete(job, jobhelper.status_succeed, thread_id=thread_id)
        loghelper.info('end:' + url, thread_id)
        job = jobhelper.next(thread_id)
    loghelper.info('end:excute({})'.format(thread_id))


for i in range(40):
    threading.Thread(target=execute, args=(i,)).start()
