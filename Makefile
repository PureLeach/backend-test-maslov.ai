include .env
export

run:
	poetry run uvicorn app.main:app --reload

fmt:
	ruff check -s --fix --exit-zero .

lint-strict:
	mypy .
	ruff check .

lint-fix: fmt lint-strict

migrate:
	poetry run python -m yoyo apply -vvv --batch --database "postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB_NAME}" ./migrations
