# FROM python:3.7-alpine
# # alpineで軽量化

# ENV LANG C.UTF-8
# ENV TZ Asia/Tokyo

# RUN apk add --update --no-cache make bash gcc g++ tzdata git\
#   && pip install --upgrade pip \
#   && pip install uvicorn==0.11.8

# ENV PYTHONUNBUFFERED 1
# ENV PYTHONPATH /app/.pip

# ADD docker/wait-for-it.sh /usr/local/bin/wait-for-it.sh
# RUN chmod +x /usr/local/bin/wait-for-it.sh

FROM tiangolo/uvicorn-gunicorn:python3.8

COPY ../../app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ../../app /app