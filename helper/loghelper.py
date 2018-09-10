import time
import os

_root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
_logs_dir = _root_dir + '/logs'
if not os.path.exists(_logs_dir):
    os.mkdir(_logs_dir)

_log_files = {}


def _get_log_file(thread_id):
    log_file_key = 'thread_' + str(thread_id)
    if log_file_key not in _log_files:
        _log_files[log_file_key] = open(_logs_dir + '/log_thread[{}]_{}.txt'.format(thread_id, time.strftime('%Y%m%d')), 'a')
    return _log_files[log_file_key]


def info(msg, thread_id=-1):
    write('[info]' + str(msg), thread_id)


def warn(msg, thread_id=-1):
    write('[warn]' + str(msg), thread_id)


def error(msg, thread_id=-1):
    write('[error]' + str(msg), thread_id)


def write(msg, thread_id=-1):
    msg = time.strftime('[%Y-%m-%d %H:%M:%S]') + msg + '\r\n'
    print(msg)
    log_file = _get_log_file(thread_id)
    log_file.write(msg)
    log_file.flush()
