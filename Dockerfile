FROM python:2.7-alpine

RUN pip install flask --no-cache-dir

ENV FLASK_APP=/main.py

COPY main.py GIT_* /

EXPOSE 5000

CMD ["/bin/sh", "-c", "python -m flask run --host=0.0.0.0"]
