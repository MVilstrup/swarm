import socket
import os
import sys
import multiprocessing
import time
import platform


def add_localhost(func):
    def inner(*args, **kwargs):
        ips = func(*args, **kwargs)
        localhost = '127.0.0.1'
        if localhost not in ips:
            ips.append(localhost)
        return ips

    return inner


@add_localhost
def get_ips():
    localIP = socket.gethostbyname(socket.gethostname())
    ex = socket.gethostbyname_ex(socket.gethostname())[2]
    if len(ex) == 1:
        return [ex[0]]
    return [ip for ip in ex if ip != localIP]


def get_ip():
    localIP = socket.gethostbyname(socket.gethostname())
    ex = socket.gethostbyname_ex(socket.gethostname())[2]
    if len(ex) == 1:
        return ex[0]
    for ip in ex:
        if ip != localIP:
            return ip


def root_dir():
    def _get_dir(f):
        return os.path.dirname(f)

    f = os.path.abspath(__file__)
    for _ in range(3):
        f = _get_dir(f)
    return f


def import_job_desc(path):
    dir_, name = os.path.split(path)
    if os.path.isfile(path):
        name = name.rstrip('.py')
    else:
        sys.path.insert(0, os.path.dirname(dir_))
    sys.path.insert(0, dir_)
    job_module = __import__(name)
    job_desc = job_module.get_job_desc()

    return job_desc


def iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False

    return True


def get_cpu_count():
    return multiprocessing.cpu_count()


def get_os_name():
    return platform.system()


def is_windows():
    return get_os_name() == 'Windows'


class Clock(object):
    def __init__(self, start=None):
        self.start = start
        if self.start is None:
            self.start = time.time()

        self.paused = 0.0
        self.is_paused = False
        self.acc_paused = 0.0

    def pause(self):
        if not self.is_paused:
            self.paused = time.time()
            self.is_paused = True

    def resume(self):
        if self.is_paused:
            self.acc_paused += time.time() - self.paused
            self.is_paused = False

    def clock(self):
        return time.time() - self.start - self.acc_paused
