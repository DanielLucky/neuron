# neuron
Тестовое задание


Запуск в контейнере
----------

Поднимите docker-compose:

```no-highlight
$ docker-compose up
```

Локальный запуск
----------

1. Поднимите PostrgeSQL в docker-compose:

```no-highlight
$ docker-compose up db
```
2. Измените DNS на локальный коннект (neuron/database/db.py, neuron/database/alembic.ini)
3. Создание виртуального окружения
```no-highlight
$ poetry env use `<Python PATH 3.9>`
$ poetry shell
$ poetry install
```
4. Выполните миграции
```no-highlight
$ cd database/; alembic revision --autogenerate -m "Initial"; alembic upgrade head; cd ..
```
5. Запустите сервер
```no-highlight
$ python main.py
```
Документация [PostmanDoc](https://documenter.getpostman.com/view/17461733/UzQvu5ck#ed002494-dca2-4264-a568-af00168b5087)
