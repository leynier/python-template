HOST = {{ cookiecutter.host }}
PORT = {{ cookiecutter.port }}

install:
	poetry install

tests: install
	poetry run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203
	poetry run black . --check
	poetry run isort . --profile=black
	poetry run pytest --cov=./ --cov-report=xml

export:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

update_index:
	cp README.md docs/index.md

run: install
	poetry run uvicorn {{ cookiecutter.pkg_name }}.main:app --reload --host ${HOST} --port ${PORT}

build:
	docker build -t {{ cookiecutter.project_slug }}:latest .

deploy:
	docker run -d -p 8000:80 --name {{ cookiecutter.project_slug }}-container --env-file .env {{ cookiecutter.project_slug }}:latest

rmcontainer:
	docker container rm {{ cookiecutter.project_slug }}-container --force

rmimage:
	docker image rm {{ cookiecutter.project_slug }}:latest

build_deploy: build deploy

rmall: rmcontainer rmimage

redeploy: rmall build_deploy

logs:
	docker logs {{ cookiecutter.project_slug }}-container
