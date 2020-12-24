#!/bin/bash

set -e

cd "$( dirname "${BASH_SOURCE[0]}" )"

pip install -r requirements.txt
gunicorn --bind 0.0.0.0:8443 --certfile=/etc/certs/tls.crt --keyfile=/etc/certs/tls.key app:app 
