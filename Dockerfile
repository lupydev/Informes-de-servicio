FROM python:3.12-slim

# Establecer el directorio
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt requirements.txt
COPY .gitignore .gitignore

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos los archivos
COPY . .

# Puerto que usara la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


