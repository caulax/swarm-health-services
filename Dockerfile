FROM python:2.7-alpine

ENV TZ "Europe/Kiev"

# set time
RUN apk add --update tzdata && \
	cp /usr/share/zoneinfo/${TZ} /etc/localtime && \
	echo ${TZ} > /etc/timezone

WORKDIR /var/app

ADD ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
