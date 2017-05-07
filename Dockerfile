FROM library/python:3-alpine

RUN mkdir /dunesea
WORKDIR /dunesea

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./* /dunesea
