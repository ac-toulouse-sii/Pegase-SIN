FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN apt update && apt install -y iproute2

RUN pip install --no-cache-dir -r requirements.txt

COPY lcd.py .

CMD ["python", "lcd.py"]