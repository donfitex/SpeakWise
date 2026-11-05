.PHONY: install check dev stop
install:
	python3 -m venv .venv
	.venv/bin/python -m pip install -r requirements.lock
	cd frontend && npm ci
check:
	.venv/bin/ruff check backend scripts
	.venv/bin/ruff format --check backend scripts
	.venv/bin/python backend/manage.py check --settings=config.settings.test
	.venv/bin/python backend/manage.py makemigrations --check --dry-run --settings=config.settings.test
	.venv/bin/python backend/manage.py spectacular --settings=config.settings.test --validate --fail-on-warn --file /tmp/speakwise-openapi.yaml
	.venv/bin/python -m pytest -q
	cd frontend && npm run lint && npm run format:check && npm test && npm run build
dev:
	python3 scripts/configure_local.py
	docker compose up --build -d --wait
	docker compose exec -T api python backend/manage.py seed_demo
stop:
	docker compose down
