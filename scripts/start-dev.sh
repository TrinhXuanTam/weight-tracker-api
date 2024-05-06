#!/usr/bin/env bash

set -e

DEFAULT_MODULE_NAME=src.main

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-9000}
DEBUG_PORT=${DEBUG_PORT:-5678}
LOG_LEVEL=${LOG_LEVEL:-info}
LOG_CONFIG=${LOG_CONFIG:-/src/logging.ini}

# Start Uvicorn with live reload
exec  python -m debugpy --listen $HOST:$DEBUG_PORT  -m uvicorn --reload --proxy-headers --host 0.0.0.0 --port 9000 --log-config $LOG_CONFIG "$APP_MODULE"