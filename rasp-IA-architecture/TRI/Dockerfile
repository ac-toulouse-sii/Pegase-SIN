FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY classes_autorisees.txt .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY tri.py .

CMD ["python", "tri.py"]