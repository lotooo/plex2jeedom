FROM python:latest
MAINTAINER Matthieu Serrepuy "lotooo@gmail.com"
ENV JEEDOM_HOST 127.0.0.1
ENV JEEDOM_API  XXXXXXXXX
ENV SCENARIO_MAPPING_YAML /config/plex2jeedom.yml
RUN mkdir /config
COPY . /app
COPY plex2jeedom.yml /config
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["plex2jeedom.py"]
