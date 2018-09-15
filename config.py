import configparser

_conf = configparser.ConfigParser()
_conf.read('config.ini')

mongodb_host = _conf.get('mongodb', 'host')
mongodb_port = _conf.getint('mongodb', 'port')

raw_data_path = _conf.get('app', 'raw_data_path')
