# coding:utf-8
import multiprocessing

# reload = True

# reload_engine = 'inotify'

# spew = True

# check_config = True

workers = multiprocessing.cpu_count()
worker_class = 'gevent'

accesslog = '/app/mnt/var/log/gunicorn/access.log'

access_log_format = '%(h)s %(u)s %(U)s'

errorlog = '/app/mnt/var/log/gunicorn/error.log'

loglevel = 'debug'

disable_redirect_access_to_syslog = True

reuse_port = True

chdir = '/app/'

daemon = False

# raw_env = ''

pidfile = '/app/mnt/run/gunicorn.pid'

# user = 'root'

bind = ['0.0.0.0:8080', 'unix:/app/mnt/run/gunicorn.sock']

workers = 1

timeout = 60
