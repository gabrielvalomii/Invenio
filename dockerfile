FROM python:3.11-slim

LABEL maintainer="gabriel"
LABEL description="Invenio - Sistema de Gerenciamento de Estoque"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    pkg-config \
    gcc \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]