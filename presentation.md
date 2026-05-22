---
marp: true
theme: uncover
paginate: true
---

# Лабораторная работа №11
Калькулятор и презентация

## Docker

        FROM python:3.14-slim
        COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
        WORKDIR /app
        COPY pyproject.toml .
        RUN uv sync --no-dev
        COPY . .
        ENV PATH="/app/.venv/bin:$PATH"
        EXPOSE 8000
        CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

Содержание Dockerfile

---

## Docker

    services:
        web:
            build: .
            ports:
                - "8000:8000"
            volumes:
                - ./db.sqlite3:/app/db.sqlite3
            command: >
                sh -c "python manage.py migrate &&
                            sh -c "python manage.py runserver 0.0.0.0:8000"



## Презентация Marp

![width:600px](image-5.png)

Результат