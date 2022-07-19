# установка базового образа (python@3.10.4)
FROM python:3.9.13
# установка рабочей директории в контейнере
WORKDIR /code
# копирование файла зависимостей в рабочую директорию
COPY . .
RUN /usr/local/bin/python -m pip install --upgrade pip
# установка poetry
RUN pip install poetry
# установка зависимостей
RUN poetry lock --no-update; poetry export -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt
# Миграции в бд
# RUN cd database/; alembic revision --autogenerate -m "Initial"; alembic upgrade head; cd ..
# команда, выполняемая при запуске контейнера
# CMD [ "python", "main.py"]