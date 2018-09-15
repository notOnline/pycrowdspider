import uuid
import config

def write(html):
    file_name = str(uuid.uuid1()).replace('-', '') + '.html'
    open(config.raw_data_path + file_name, 'w', encoding='utf-8').write(html)
    return file_name


