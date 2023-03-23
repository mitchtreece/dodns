FROM python:3-alpine
MAINTAINER Mitch Treece <mitchtreece@me.com>
RUN mkdir /app
COPY . /app/
WORKDIR /app
RUN pip3 install requirements.txt
ENTRYPOINT ["python", "/app/dodns.py"]