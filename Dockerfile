FROM python:3-alpine
MAINTAINER Mitch Treece <mitchtreece@me.com>

# Setup Directories

RUN mkdir /app
COPY init.sh /app/
COPY dodns.py /app/
COPY requirements.txt /app/
WORKDIR /app

# Permissions

RUN chmod +x init.sh

# Install Dependencies

RUN pip3 install -r requirements.txt

# Run

ENTRYPOINT ["./init.sh"]