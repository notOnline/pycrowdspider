import hashlib


def md5hash(str_value):
    md5 = hashlib.md5()
    md5.update(str_value.encode('utf-8'))
    return md5.hexdigest()
