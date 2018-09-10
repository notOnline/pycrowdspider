from helper import db


db.add_job_one({
    "url": 'https://book.douban.com/tag/',
    "extractor": 'douban_tag_extractor',
    "status": 0,
    "job_args": {"url": 'https://book.douban.com/tag/'}
})

