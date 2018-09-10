import re

ip_reg = '^(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|[1-9]).(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|[1-9]).(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|[1-9]).(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|[1-9])$'
from helper import db

for proxy in db.get_all('proxies'):
    if not re.match(ip_reg, proxy['ip']):
        db.delete_one('proxies', {'_id': proxy['_id']})