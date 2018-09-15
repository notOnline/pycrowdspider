import threading
from threading import Lock
from downloader import downloader
from helper import db, loghelper, filehelper, jobhelper
import config

_locker_proxyhelper: Lock = threading.Lock()
_job_status_init = -1
_job_status_succeed = 1
_job_status_failed = -2


def execute():
    job = jobhelper.next()
    while job is not None:
        url = job['url']
        loghelper.info('start:' + url)
        model = db.raw_data.find_one({'url': url})
        if model:
            html = open(config.root_path + model['html_file_path'], 'r', encoding='utf-8').read()
        else:
            html = downloader.download(url, auto_protocol=job['auto_protocol'])
            html_file_path = filehelper.write(html)
            db.raw_data.insert_one({'url': url, 'html_file_path': html_file_path})
        extractor = __import__('extractor', globals(), locals(), [job['extractor']])
        real_extractor = eval('extractor.' + job['extractor'])
        try:
            real_extractor.extract(html=html, job_args=job['job_args'], url=url)
        except Exception as msg:
            loghelper.error(msg)
            jobhelper.complete(job, jobhelper.status_failed)
        else:
            jobhelper.complete(job, jobhelper.status_succeed)
        loghelper.info('end:' + url)
        job = jobhelper.next()


for i in range(30):
    threading.Thread(target=execute).start()
