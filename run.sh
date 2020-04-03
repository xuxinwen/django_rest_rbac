#!/usr/bin/env bash

python init_mnt_dirs.py && python manage.py migrate && supervisord -c /etc/supervisor/supervisord.conf --nodaemon
