
import uuid
import os


def write(html):
    html_file_path = 'data/' + str(uuid.uuid1()).replace('-', '') + '.html'
    open(os.path.abspath(html_file_path), 'w', encoding='utf-8').write(html)
    return html_file_path