FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

ENV CONF=/app/conf.py

COPY ./app /app
