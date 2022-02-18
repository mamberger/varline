import multiprocessing
from uvicorn.workers import UvicornWorker

bind = '127.0.0.1:8000'
workers = multiprocessing.cpu_count() * 2 + 1
# user = 'root'
# backlog = 20480
worker_class = 'uvicorn.workers.UvicornCustomWorker'
# accesslog = '-'
# preload_app = True
# loglevel = 'error'
# max_requests = 32
# timeout = 5
#graceful_timeout = 5
