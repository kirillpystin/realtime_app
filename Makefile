info:
	@echo "make run	- Запуск приложения"
	@echo "make install	- Установка всех зависимостей"
	@echo "make build	- Сборка докера"
	@echo "make install_front	- Установка зависимостей для клиента"
	@echo "make run_front	- Запуск клиента"
	@exit 0

run:
	 poetry run run_server

build:
	docker-compose -f docker-compose.yaml up -d --build

install:
	pip install poetry
	poetry install


install_front:
	cd front/front && npm install

run_front:
	cd front/front && npm start