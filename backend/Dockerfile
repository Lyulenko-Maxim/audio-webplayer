FROM python:3.11.5-alpine

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
