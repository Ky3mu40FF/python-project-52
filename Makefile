MANAGE := poetry run python manage.py

.PHONY: test
test:
	@poetry run pytest

.PHONY: test-coverage
test-coverage:
	@poetry run pytest --cov=page_loader --cov-report xml

.PHONY: setup
setup: db-clean install migrate

.PHONY: install
install-dev:
	@poetry install

.PHONY: db-clean
db-clean:
	@rm db.sqlite3 || true

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

.PHONY: lint
lint:
	@poetry run flake8 task_manager
