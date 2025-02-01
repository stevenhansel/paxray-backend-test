FROM python:3.12.2-bookworm

WORKDIR /app

RUN apt-get update
RUN apt-get install -y sqlite3

RUN pip3 install flask flask_sqlalchemy pandas 

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
