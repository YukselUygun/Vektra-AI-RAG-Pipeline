FROM apache/airflow:2.9.3-python3.10

# Root yetkisi al 
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Tekrar Airflow kullanıcısına dön 
USER airflow

# Kütüphaneleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt