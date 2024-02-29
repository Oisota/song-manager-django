FROM python:3.10.13-bookworm

WORKDIR /opt/app

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry && poetry install --only main --no-root --no-directory

COPY . .

CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "songmanager.wsgi:application"]