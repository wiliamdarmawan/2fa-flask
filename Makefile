docker-up:
	docker-compose up --build -d
docker-down:
	docker-compose down --remove-orphans --volumes
docker-reset:
	make docker-down
	make docker-up
test:
	docker-compose --profile test build
	docker-compose --profile test run --rm test pytest tests/