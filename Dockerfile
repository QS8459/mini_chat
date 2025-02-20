FROM python:3.11-alpine

WORKDIR /app

COPY . .

COPY requirements.txt /app

RUN pip install -r requirements.txt
RUN mkdir alembic
#RUN alembic init alembic

RUN alembic revision --autogenerate -m "INIT" &&\
    alembic upgrade head

EXPOSE 5000
