#!/bin/bash

if [ "$1" = "run_celery" ]; then
  celery -A worker.celery worker -Q celery,high_priority --loglevel=info --logfile=logs/celery.log
fi

if [ "$1" = "run_flower" ]; then
   python --version && which python
   python -m celery
  celery -A worker.celery flower --port=5555 --loglevel=debug
fi

if [ "$1" = "run_server" ]; then
  python --version && which python
  echo "Run server"
  exec gunicorn main:app --preload --config file:gunicorn.conf.py -b 0.0.0.0:5000
  # exec gunicorn app.main:app --config file:gunicorn.conf.py
fi
