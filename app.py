import os
import pandas as pd
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dataclasses import dataclass


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"sqlite:///{os.path.join(basedir, 'testdata.db')}"

db = SQLAlchemy(app)

#### SPACE FOR DATABASE STUFF ####


@dataclass
class AppLog(db.Model):
    __tablename__ = "applog"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestarted: Mapped[datetime] = mapped_column(nullable=False)
    timeended: Mapped[datetime] = mapped_column(nullable=False)
    userid: Mapped[str] = mapped_column(nullable=False)
    applicationname: Mapped[str] = mapped_column(nullable=False)
    windowtitle: Mapped[str] = mapped_column(nullable=False)


@dataclass
class UILog(db.Model):
    __tablename__ = "uilog"

    id: Mapped[int] = mapped_column(primary_key=True)
    userid: Mapped[str] = mapped_column(nullable=False)
    appid: Mapped[str] = mapped_column(nullable=False)
    eventtype: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    acceleratorkey: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)

    app_log = relationship(
        "AppLog",
        primaryjoin="and_(UILog.appid == foreign(AppLog.id), UILog.userid == foreign(AppLog.userid))",
    )


#### SPACE FOR API ENDPOINTS ####


@app.route("/")
def index():
    return {"message": "Hello, World!"}


@app.route("/copyPasteAnalysis")
def copyPasteAnalysis():
    query = (
        UILog.query.join(UILog.app_log)
        .with_entities(
            UILog.timestamp,
            UILog.name,
            UILog.eventtype,
            AppLog.applicationname,
            UILog.userid,
        )
        .filter(
            or_(
                UILog.eventtype.in_(["CTRL + C", "CTRL + X", "CTRL + V"]),
                and_(UILog.eventtype == "Left-Down", UILog.acceleratorkey == "STRG+C"),
            )
        )
        .order_by(UILog.timestamp)
    )
    data = query.all()

    print(data)

    # TODO: Perform aggregation with pandas
    _df = pd.DataFrame(data)
    """

    """

    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
