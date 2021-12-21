FROM python:3.7-slim
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./code /code
ENTRYPOINT python main.py
