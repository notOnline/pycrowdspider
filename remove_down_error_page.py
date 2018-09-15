from helper import db
from downloader import downloader

for job in list(db.jobs.find({'status': 0})):
    url=job['url']
    model = db.raw_data.find_one({'url': url})
    if model:
        html = open(model['html_file_path'], 'r', encoding='utf-8').read()
        if '页面不存在' in html:
            db.raw_data.delete_one({'url': job['url']})
            print('delete:' + job['url'])
    db.jobs.update_one({'_id':job['_id']},{'$set':{'status':-100}})