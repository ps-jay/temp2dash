FROM python:2

MAINTAINER Philip Jay <phil@jay.id.au>

ENV TZ Australia/Melbourne

RUN pip install -U pip requests https://github.com/ps-jay/temper-python/archive/devel.zip

RUN mkdir /opt/temp2dash
ADD *.py /opt/temp2dash/

CMD [ "python", "/opt/temp2dash/temp2dash.py" ]
