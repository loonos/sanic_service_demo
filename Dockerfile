FROM python:3.7-slim
COPY ./code/ /code/
WORKDIR /code

RUN apt-get update
RUN apt-get install --no-install-recommends -y vim curl
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements.txt

ENTRYPOINT python main.py
