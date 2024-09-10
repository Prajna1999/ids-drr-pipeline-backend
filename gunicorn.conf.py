import multiprocessing
workers = multiprocessing.cpu_count()*2+1

bind = "0.0.0.0:8080"

try:
    import gevent
    worker_class = "gevent"
except ImportError:
    worker_class = "sync"

timeout = 120

loglevel = "info"
