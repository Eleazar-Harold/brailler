#!/usr/bin/env bash

set -x

mypy brl
black --check brl
isort --recursive --check-only brl
flake8 brl --max-line-length=88 # --exclude = .git,__pycache__,__init__.py,.mypy_cache,.pytest_cache
