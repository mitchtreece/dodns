FROM python:3-alpine
MAINTAINER Mitch Treece <mitchtreece@me.com>
RUN mkdir /app
COPY dodns.py /app/
COPY requirements.txt /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python", "/app/dodns.py"]