# Usa una imagen oficial de Python
FROM python:3.13-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usa tu servidor Flask
EXPOSE 5000

# Comando para ejecutar tu aplicación Flask
CMD ["python", "main.py"]
