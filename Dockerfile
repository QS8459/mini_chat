FROM python:3.11-alpine

WORKDIR /app

COPY . .

COPY requirements.txt /app

RUN pip install --no-cache -r  requirements.txt
#RUN mkdir alembic
#RUN alembic init alembic

RUN chmod -x script.sh

#RUN #alembic revision --autogenerate -m "INIT" &&\
#    alembic upgrade head

EXPOSE 5000
