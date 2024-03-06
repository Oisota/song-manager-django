FROM python:3.10.13-bookworm

WORKDIR /opt/app

RUN useradd -m -r user && chown user /opt/app

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry && poetry install --only main --no-root --no-directory

COPY . .

USER user

EXPOSE 8000

WORKDIR /opt/app/songmanager

CMD ["poetry", "run", "gunicorn", "--bind", ":8000", "--workers", "4", "songmanager.wsgi:application"]