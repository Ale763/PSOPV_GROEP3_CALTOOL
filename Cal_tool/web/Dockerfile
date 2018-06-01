FROM alpine:3.7

# Initialize
RUN mkdir -p /data/web
WORKDIR /data/web
COPY requirements.txt /data/web/

# Setup
RUN apk update
RUN apk upgrade
RUN apk add --update python3 python3-dev postgresql-client postgresql-dev libffi-dev tzdata build-base gettext uwsgi
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

#Fix timezone
#RUN cp /usr/share/zoneinfo/Europe/Brussels /etc/localtime
#RUN echo "Europe/Brussels" >  /etc/timezone
#RUN apk del tzdata
#RUN crond && crontab -l

# Clean
RUN apk del -r python3-dev postgresql

# Prepare
COPY . /data/web/
RUN mkdir -p Project/static/admin



