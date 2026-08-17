FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y libglib2.0-0 libgl1 && \
    rm -rf /var/lib/apt/lists/*

COPY classes_autorisees.txt .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY tri.py .

CMD ["python", "tri.py"]