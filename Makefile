up-d:
	cd ci/docker; docker compose up -d

up-d-build:
	cd ci/docker; docker compose up -d --build --remove-orphans

logsf-backend:
	cd ci/docker; docker compose logs -f the_way_of_the_sword-backend

logsf-rmq:
	cd ci/docker; docker compose logs -f the_way_of_the_sword-mq:

exec-mq:
	cd ci/docker; docker compose exec the_way_of_the_sword-mq bash

exec-backend:
	cd ci/docker; docker compose exec the_way_of_the_sword-backend bash

exec-db:
	cd ci/docker; docker compose exec the_way_of_the_sword-db bash