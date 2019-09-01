FROM gcr.io/cw-web-service/sandbox/python-base:latest

WORKDIR /app

ADD requirement.txt .

RUN pip install -r requirement.txt

COPY . /app

ENV FLASK_APP=mainapp.py

ENV FLASK_ENV=docker

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]