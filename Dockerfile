FROM python:3.11-slim

WORKDIR /app

# 系统依赖 + cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN crontab crontab

CMD ["cron","-f"]