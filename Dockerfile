FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir logs/
RUN mkdir files/

COPY . .
ENV FLASK_APP=src/app.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
