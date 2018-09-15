# coding:utf-8
from bs4 import BeautifulSoup
from helper import db, loghelper
import re


def extract(html, job_args, url):
    soup = BeautifulSoup(html, 'html.parser')
    book_detail = {}
    book_detail['name'] = soup.select_one('#wrapper > h1').get_text().strip()
    book_detail['mainpic_href'] = soup.select_one('#mainpic > a').attrs['href']
    _info_txt = soup.select_one('#info').get_text().replace('\n', ';').replace(' ', '')

    def get_text_by_name(name, _txt):
        try:
            return re.search(name + ':;*[^;]+;', _txt).group().replace(name + ':', '').replace(';', '')
        except Exception as msg:
            loghelper.warn(msg)
            return ''

    _book_id = re.search('\d+', url).group()
    book_detail['book_id'] = _book_id
    book_detail['author'] = get_text_by_name('作者', _info_txt)
    book_detail['publish_company'] = get_text_by_name('出版社', _info_txt)
    book_detail['publish_year_month'] = get_text_by_name('出版年', _info_txt)
    book_detail['page_size'] = get_text_by_name('页数', _info_txt)
    book_detail['price'] = get_text_by_name('定价', _info_txt)
    book_detail['binding'] = get_text_by_name('装帧', _info_txt)
    book_detail['ISBN'] = get_text_by_name('ISBN', _info_txt)
    book_detail['translator'] = get_text_by_name('译者', _info_txt)
    book_detail['rating_num'] = soup.select_one('#interest_sectl  .rating_num').get_text().strip()
    if len(soup.select('#interest_sectl  .rating_per')) == 5:
        book_detail['rating_5_per'] = soup.select('#interest_sectl  .rating_per')[0].text
        book_detail['rating_4_per'] = soup.select('#interest_sectl  .rating_per')[1].text
        book_detail['rating_3_per'] = soup.select('#interest_sectl  .rating_per')[2].text
        book_detail['rating_2_per'] = soup.select('#interest_sectl  .rating_per')[3].text
        book_detail['rating_1_per'] = soup.select('#interest_sectl  .rating_per')[4].text
    if soup.select_one('.rating_people span'):
        book_detail['rating_people'] = soup.select_one('.rating_people span').text

    def get_related_info(node):
        if '内容简介' in node.prettify():
            return ('content_brief_intro_html', soup.select('#link-report  .intro')[-1].prettify())
        if '作者简介' in node.prettify():
            return ('author_brief_intro_html',node.find_next_sibling(attrs={'class':'indent'}).prettify())
        if '目录' in node.prettify():
            dir_html = ''
            if soup.select_one('#dir_{}_full'.format(_book_id)):
                dir_html = soup.select_one('#dir_{}_full'.format(_book_id)).prettify()
            return ('dir_html', dir_html)
        return ('', '')

    for h2_node in soup.select('.related_info h2'):
        item_name, item_value = get_related_info(h2_node)
        if item_name != '':
            book_detail[item_name] = item_value


    also_like_book_ids = []
    for also_like_book in soup.select('#db-rec-section dd a'):
        also_like_book_ids.append(re.search('\d+', also_like_book.attrs['href']).group())

    book_detail['also_like_book_ids'] = also_like_book_ids
    db.book_details.insert_one(book_detail)

    db.jobs.insert_one({'url': url + 'comments/',
                        'extractor': "douban_book_comments_extractor",
                        'status': 0,
                        'auto_protocol': False,
                        'job_args':
                            {
                                'tag_name': job_args['tag_name']
                            }
                        })


def get_tag_text(tag):
    if tag:
        return tag.text
    else:
        return ''
