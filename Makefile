up-d:
	cd ci/docker; docker compose up -d

up-d-build:
	cd ci/docker; docker compose up -d --build --remove-orphans

build-scheduler-worker:
	cd ci/docker; docker compose up -d --build --remove-orphans the_way_of_the_sword-taskiq-scheduler the_way_of_the_sword-taskiq-worker

logsf-backend:
	cd ci/docker; docker compose logs -f the_way_of_the_sword-backend

logsf-rmq:
	cd ci/docker; docker compose logs -f the_way_of_the_sword-mq

logsf-scheduler:
	cd ci/docker; docker compose logs -f the_way_of_the_sword-taskiq-scheduler

logsf-worker:
	cd ci/docker; docker compose logs -f the_way_of_the_sword-taskiq-worker

exec-mq:
	cd ci/docker; docker compose exec the_way_of_the_sword-mq bash

exec-backend:
	cd ci/docker; docker compose exec the_way_of_the_sword-backend bash

exec-db:
	cd ci/docker; docker compose exec the_way_of_the_sword-db bash