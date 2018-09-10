import os

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/data_pycrowdspider'
logs_dir = root_dir + '/logs'
ocr_dir = root_dir + '/ocr'
for _dir in [root_dir, logs_dir, ocr_dir]:
    if not os.path.exists(_dir):
        os.mkdir(_dir)
