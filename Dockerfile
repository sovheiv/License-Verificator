FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN apt-get update \
    && apt-get -y install libpq-dev gcc 
RUN pip install -r requirements.txt
EXPOSE 8002
CMD gunicorn -w 1 -b 0.0.0.0:8002 --timeout 3600 "run_server:app"
