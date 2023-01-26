install:
	@ pip install -r requirements.txt -r requirements-dev.txt

list-outdated: install
	@ pip list -o

lint-check:
	@ lint --directory ./pablo

lint-check-ci:
	@ lint --directory ./pablo --output-file lint-check-results.json --output-format annotations

lint-fix:
	@ isort --sl -l 1000 ./pablo
	@ lint --directory ./pablo

type-check:
	@ type-check --directory ./pablo

type-check-ci:
	@ type-check --directory ./pablo --output-file type-check-results.json --output-format annotations

security-check:
	@ security-check --directory ./pablo

security-check-ci:
	@ security-check --directory ./pablo --output-file security-check-results.json --output-format annotations

build:
	@ echo "Not Supported"

start:
	@ uvicorn application:app --host 0.0.0.0 --port 5000 --no-access-log --reload

start-prod:
	@ uvicorn application:app --host 0.0.0.0 --port 5000 --no-access-log

start-worker:
	@ python3 worker.py

start-worker-prod:
	@ python3 worker.py

test:
	@ echo "Not Supported"

clean:
	@ rm -rf ./.mypy_cache ./__pycache__ ./build ./dist

.PHONY: *
