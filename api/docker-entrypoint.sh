#!/bin/sh
./wait-for-it.sh redis:6379 -t 10 -- echo "redis is up"
./wait-for-it.sh redis:5432 -t 10 -- echo "postgres is up"
flake8
cd src
alembic upgrade head
python3 -m pytest -v -s -p no:warnings ../tests
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

