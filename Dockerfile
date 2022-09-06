FROM python:3.8-slim-buster
WORKDIR /code
COPY ./flask_app/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./flask_app/ .
CMD ["flask", "run", "--host", "0.0.0.0", "--port=80"]