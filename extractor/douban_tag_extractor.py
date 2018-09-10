def extract(html, job_args):
    from bs4 import BeautifulSoup
    from helper import db

    soup = BeautifulSoup(html, 'html.parser')
    douban_tags = []
    jobs = []
    for div_node in soup.select('#content > div > div.article > div:nth-of-type(2) > div'):
        ptagname = div_node.findChild('a').attrs['name']
        for tag_node in div_node.select('td'):
            tag_name = tag_node.findChild('a').text
            tag_href = 'https://book.douban.com' + tag_node.findChild('a').attrs['href'] + '?start=0&type=R'
            tag_comment_count = tag_node.findChild('b').text.replace('(', '').replace(')', '')
            douban_tags.append({
                "name": tag_name,
                "href": tag_href,
                "comment_count": tag_comment_count,
                "ptagname": ptagname
            })
            jobs.append({
                "url": tag_href,
                "extractor": 'douban_book_brief_extractor',
                "status": 0,
                "auto_protocol": False,
                "job_args": {"url": tag_href, 'tag_name': tag_name}
            })
            jobs.append({
                "url": tag_href.replace('type=R','type=S'),
                "extractor": 'douban_book_brief_extractor',
                "status": 0,
                "auto_protocol": False,
                "job_args": {"url": tag_href, 'tag_name': tag_name}
            })
            jobs.append({
                "url": tag_href.replace('type=R','type=T'),
                "extractor": 'douban_book_brief_extractor',
                "status": 0,
                "auto_protocol": False,
                "job_args": {"url": tag_href, 'tag_name': tag_name}
            })
    db.douban_tags.insert_many(douban_tags)
    db.jobs.insert_many(jobs)
