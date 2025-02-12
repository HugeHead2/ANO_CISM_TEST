Для запуска необходим docker и docker-compose

Порядок команд:
docker-compose build
docker-compose up postgres rabbimq
docker-compose up run_migrations
docker-compose up server start_worker

Для запуска тестов: docker-compose up tests
