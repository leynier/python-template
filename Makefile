HOST = localhost
PORT = 8000

install:
	poetry install

tests: install
	poetry run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203
	poetry run black . --check
	poetry run isort . --profile=black
	poetry run pytest --cov=./ --cov-report=xml

export:
	poetry export -f requirements.txt -o requirements.txt

export_and_commit: export
	git config --global user.name 'leynier'
	git config --global user.email 'leynier41@gmail.com'
	git add requirements.txt
	git commit --allow-empty -m "Update requirements.txt"
	git push

update_index:
	cp README.md docs/index.md

update_index_and_commit: update_index
	git config --global user.name 'leynier'
	git config --global user.email 'leynier41@gmail.com'
	git add docs/index.md
	git commit --allow-empty -m "Update docs/index.md"
	git push

run: install
	poetry run uvicorn template.main:app --reload --host ${HOST} --port ${PORT}

build:
	docker build -t template:latest .

deploy:
	docker run -d -p 8000:80 --name template-container --env-file .env template:latest

rmcontainer:
	docker container rm template-container --force

rmimage:
	docker image rm template:latest

build_deploy: build deploy

rmall: rmcontainer rmimage

redeploy: rmall build_deploy
