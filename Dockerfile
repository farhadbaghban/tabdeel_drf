FROM python:3.8.10

WORKDIR /code

COPY requirements.txt /code/


RUN pip install -U pip && pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD [ "gunicorn","tabdeel_drf.wsgi",":8000" ]
