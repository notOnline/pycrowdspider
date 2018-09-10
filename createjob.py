from helper import db


def create_douban_book_tag_job():
    db.jobs.insert_one({
        "url": 'https://book.douban.com/tag/',
        "extractor": 'douban_tag_extractor',
        "status": 0,
        "auto_protocol": False,
        "job_args": {"url": 'https://book.douban.com/tag/'}
    })


def create_douban_book_detail_job():
    print(1)


def create_douban_book_tag_S_T_from_R():
    compeleted_jobs=db.jobs.find({'status':1})
    print(compeleted_jobs.count())
    for job in compeleted_jobs:
        if job['url'].endswith('type=R'):
            db.jobs.insert_one({
                'url':job['url'].replace('type=R','type=S'),
                'extractor':job['extractor'],
                'status':0,
                'auto_protocol':False,
                'job_args':{
                    'url':job['url'].replace('type=R','type=S'),
                    'tag_name':job['job_args']['tag_name']
                }
            })
            db.jobs.insert_one({
                'url': job['url'].replace('type=R', 'type=T'),
                'extractor': job['extractor'],
                'status': 0,
                'auto_protocol': False,
                'job_args': {
                    'url': job['url'].replace('type=R', 'type=T'),
                    'tag_name': job['job_args']['tag_name']
                }
            })
create_douban_book_tag_S_T_from_R()
