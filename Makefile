up-bg:
	docker-compose up -d

up:
	docker-compose up

kill:
	docker-compose kill

build:
	docker-compose build

logs:
	docker compose logs weight_tracker_api $(args)

ps:
	docker-compose ps

exec:
	docker-compose exec weight_tracker_api $(args)

ruff:
	docker-compose exec weight_tracker_api ruff $(args) src

black:
	docker-compose exec weight_tracker_api black src

lint: ruff black

db-make-migration:
	docker compose exec weight_tracker_api alembic revision --autogenerate -m "$(args)"

db-migrate:
	docker compose exec weight_tracker_api alembic upgrade head

db-downgrade:
	docker compose exec weight_tracker_api alembic downgrade $(args)