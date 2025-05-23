# Usa una imagen oficial de Python
FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    build-essential \
    pkg-config \
    postgresql-client

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY requirements.txt /app/

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

