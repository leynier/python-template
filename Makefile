export:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

tests: install
	poetry run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203
	poetry run black . --check
	poetry run isort . --profile=black
	poetry run pytest --cov=./ --cov-report=xml

install:
	poetry install
