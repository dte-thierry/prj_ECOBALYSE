# extract/Dockerfile
FROM python:3

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install --no-cache-dir requests

CMD ["python3", "ecbl_extract.py"]
