FROM python:3-alpine

RUN pip install flask --no-cache-dir && \
    addgroup -S -g 2222 yadi && \
    adduser -S -u 2222 -g yadi yadi
    
COPY main.py GIT_* /

RUN chmod 755 /main.py

USER yadi

ENV FLASK_APP=/main.py

EXPOSE 5000

CMD ["/bin/sh", "-c", "python -m flask run --host=0.0.0.0"]