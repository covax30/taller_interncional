FROM python:3.11-slim

# Evitar que Python genere archivos .pyc y asegurar que los logs salgan en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalación de dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Dependencias para mysqlclient
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    # Dependencias esenciales para WeasyPrint, Cairo y ReportLab
    libcairo2-dev \
    libpango1.0-dev \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    # Fuentes comunes para que los PDF no salgan con errores de renderizado
    fonts-liberation \
    # Herramientas de compilación para paquetes como bcrypt/cryptography
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Actualizar pip e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]