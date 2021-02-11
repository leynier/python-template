install:
	poetry install

tests: install
	poetry run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203
	poetry run black . --check
	poetry run isort . --profile=black
	poetry run pytest --cov=./ --cov-report=xml

export:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

export_and_commit: export
	git config user.name '{{ cookiecutter.github_username }}'
	git config user.email '{{ cookiecutter.email }}'
	git add requirements.txt
	git commit --allow-empty -m "Update requirements.txt"
	git push

update_index:
	cp README.md docs/index.md

update_index_and_commit: update_index
	git config user.name '{{ cookiecutter.github_username }}'
	git config user.email '{{ cookiecutter.email }}'
	git add docs/index.md
	git commit --allow-empty -m "Update docs/index.md"
	git push
