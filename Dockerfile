FROM library/alpine

RUN mkdir /dunesea
WORKDIR /dunesea

ENV FLASK_APP=dunesea.py
ENV STORAGE_LOCATION=/dunesea/storage

VOLUME /dunesea/storage

RUN apk -U upgrade \
  && apk add python3 py3-flask \
  && rm -rf /tmp/* /var/cache/apk/*

COPY dunesea.py /dunesea/

EXPOSE 5000

CMD flask run
