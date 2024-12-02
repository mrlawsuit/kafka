FROM python:3.8-slim

COPY main.py /app/main.py

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

ENTRYPOINT ["python3", "main.py"]
