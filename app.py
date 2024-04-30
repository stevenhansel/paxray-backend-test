from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdata.db'
db = SQLAlchemy(app)


#### SPACE FOR DATABASE STUFF ####

@dataclass
class AppLog(db.Model):
    __tablename__ = 'applog'
    # TODO

@dataclass
class UILog(db.Model):
    __tablename__ = 'uilog'
    # TODO


#### SPACE FOR API ENDPOINTS ####


@app.route('/')
def index():
    return {"message": "Hello, World!"}

@app.route('/copyPasteAnalysis')
def copyPasteAnalysis():
    # TODO
    return {}

    
if __name__ == "__main__":
    app.run(debug=True)