FROM python:3-alpine

RUN pip install docker-compose flask gunicorn
ADD webhook-compose.py .
COPY webhook-compose.conf.dist webhook-compose.conf
CMD [ "gunicorn", "-b", ":80", "--access-logfile", "-", "--error-logfile", "-", "webhook-compose:app" ]
