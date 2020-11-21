FROM python:3
RUN pip install flask sqlalchemy psycopg2 pytz


COPY flask_api /flask_api

WORKDIR flask_api