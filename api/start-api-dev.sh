#!/usr/bin/env bash
set -e -o pipefail

exec uvicorn application:app --host 0.0.0.0 --port 5000 --no-access-log --reload
