FROM ubuntu:latest
MAINTAINER Tang Li Qun "tliqun@gmail.com"
RUN apt-get update -y && apt-get install -y python3-pip python3-dev build-essential \
&& apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8
COPY . /app
#EXPOSE 5000
WORKDIR /app
RUN pip3 install -r aodh-backend/requirements.txt
ENV LANG C.UTF-8
CMD cd aodh-backend && gunicorn --bind 0.0.0.0:$PORT wsgi
#CMD python3 app.py
