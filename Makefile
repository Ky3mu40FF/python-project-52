MANAGE := poetry run python manage.py

.PHONY: test
test:
	@poetry run pytest

.PHONY: test-coverage
test-coverage:
	@poetry run pytest --cov=task_manager --cov-report xml

.PHONY: setup
setup: db-clean install migrate

.PHONY: install
install:
	@poetry install --no-root

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
