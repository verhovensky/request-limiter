#!/bin/bash

echo "Run server"
exec gunicorn app.main:app --config file:gunicorn.conf.py