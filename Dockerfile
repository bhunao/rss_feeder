FROM python:3.11-slim-buster
 
WORKDIR /app
 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
 
# install system dependencies
RUN apt-get update \
  && apt-get clean
 
# install python dependencies
RUN pip install psycopg2-binary
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip uninstall pyjwt[crypto]
RUN pip uninstall cryptography
RUN pip install -r requirements.txt
 
COPY . /app

# RUN pytest
