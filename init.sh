#!/bin/bash

if [ "$1" = "run_celery" ]; then
  celery -A worker.celery worker -Q celery,high_priority --loglevel=info --logfile=logs/celery.log
fi

if [ "$1" = "run_flower" ]; then
  celery -A worker.celery --broker=redis://redis flower --port=5555 --address=0.0.0.0 --loglevel=debug
fi

if [ "$1" = "run_server" ]; then
  echo "Run server"
  exec gunicorn main:app --config file:gunicorn.conf.py
fi
