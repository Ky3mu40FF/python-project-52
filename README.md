# Task Manager

## Status

### Hexlet tests and linter status

[![Actions Status](https://github.com/Ky3mu40FF/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/Ky3mu40FF/python-project-52/actions)

### CodeClimate Maintainability and Test Coverage status

[![Maintainability](https://api.codeclimate.com/v1/badges/43afec8fa283efb83662/maintainability)](https://codeclimate.com/github/Ky3mu40FF/python-project-52/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/43afec8fa283efb83662/test_coverage)](https://codeclimate.com/github/Ky3mu40FF/python-project-52/test_coverage)

### Internal tests and linter status

[![Tests](https://github.com/Ky3mu40FF/python-project-52/workflows/run%20tests/badge.svg)](https://github.com/Ky3mu40FF/python-project-52/actions)
[![Linter](https://github.com/Ky3mu40FF/python-project-52/workflows/lint%20check/badge.svg)](https://github.com/Ky3mu40FF/python-project-52/actions)

## Requirements

* Python 3.10+
* [Poetry](https://python-poetry.org)
* GNU Make

## Setup

```bash
git clone git@github.com:Ky3mu40FF/python-project-52.git
cd ./python-project-52
# Create and fill .env file.
# View .env.example for reference.
curl -sSL https://install.python-poetry.org | python3 -
make setup
make test
# Run development server:
poetry run python manage.py runserver
```

---

This repository is for educational project at Hexlet course Python Developer.
This project is simple web-based Task manager based on Python Django.

Deployed service is [here](https://python-project-52-production-39fb.up.railway.app/).
