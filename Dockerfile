FROM python:3.12.2-bookworm

RUN pip3 install flask flask_sqlalchemy pandas 

WORKDIR /app

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
