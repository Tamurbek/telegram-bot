FROM python:3.11-slim

# Sistem paketlari
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    dos2unix \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependence
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# ENTRYPOINT SH fajlini alohida ko'chiramiz (ustidan yozilmasligi uchun)
COPY entrypoint.sh /app/entrypoint.sh

# CRLF → LF va execute ruxsatlari
RUN dos2unix /app/entrypoint.sh && \
    chmod 755 /app/entrypoint.sh

# Endi qolgan barcha fayllarni ko'chiramiz
COPY . /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/app/entrypoint.sh"]