def extract(html, job_args):
    from bs4 import BeautifulSoup
    from helper import db
    import re

    soup = BeautifulSoup(html, 'html.parser')
    next_page = soup.select_one('#subject_list > div.paginator > span.next  a')
    if next_page is not None:
        next_page_url = 'https://book.douban.com' + next_page.attrs['href']
        db.jobs.insert_one({
            "url": next_page_url,
            "extractor": 'douban_book_brief_extractor',
            "status": 0,
            "auto_protocol": False,
            "job_args": {"url": next_page_url, 'tag_name': job_args['tag_name']}
        })
    jobs = []
    books = []
    for item in soup.select('#subject_list > ul > li'):
        book = {}
        book['tag_name'] = job_args['tag_name']
        book['pic'] = item.select_one('.pic img').attrs['src']
        book['href'] = item.select_one('.pic a').attrs['href']
        book['name'] = get_tag_text(item.select_one('.info > h2 > a')).replace('\n', '').strip(' ')
        book['pub'] = get_tag_text(item.select_one('.pub')).replace('\n', '').strip(' ')
        book['rating_nums'] = get_tag_text(item.select_one('.rating_nums')).replace('\n', '').strip(' ')
        comment_nums_re = re.search('\d+', get_tag_text(item.select_one('.pl')))
        comment_nums = -1
        if comment_nums_re:
            comment_nums = comment_nums_re.group(0)
        book['comment_nums'] = comment_nums
        book['brief_content'] = get_tag_text(item.select_one('.info > p'))
        books.append(book)

        jobs.append({
            "url": book['href'],
            "extractor": 'douban_book_detail_extractor',
            "status": -100,
            "auto_protocol": False,
            "job_args": {'tag_name': book['tag_name']}
        })

    db.book_briefs.insert_many(books)
    db.jobs.insert_many(jobs)


def get_tag_text(tag):
    if tag:
        return tag.text
    else:
        return ''
