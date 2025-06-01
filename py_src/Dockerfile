FROM python:3.12-slim



RUN apt-get update && apt-get install -y git && apt-get clean


WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN python prepare.py
RUN pip install --no-cache-dir .

CMD granian --interface asgi API:app --host=0.0.0.0 --reload