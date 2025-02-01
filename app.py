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
    data = (
        UILog.query.join(UILog.app_log)
        .with_entities(
            UILog.timestamp,
            UILog.eventtype,
            UILog.userid,
            UILog.acceleratorkey,
            AppLog.applicationname,
        )
        .filter(
            or_(
                UILog.eventtype.in_(["CTRL + C", "CTRL + X", "CTRL + V"]),
                and_(UILog.eventtype == "Left-Down", UILog.acceleratorkey == "STRG+C"),
            )
        )
        .order_by(UILog.timestamp)
        .all()
    )

    df = pd.DataFrame(data)

    """
    Add another auxiliary column 'from_applicationname',
    to prefill the application name of the last copied/cut eventtype into all of the rows
    """
    df["from_applicationname"] = (
        df["applicationname"]
        .where(
            df["eventtype"].isin(["CTRL + C", "CTRL + X"])
            | ((df["eventtype"] == "Left-Down") & (df["acceleratorkey"] == "STRG+C"))
        )
        .groupby(df["userid"])
        .ffill()
    )

    """
    Filter such that df only contains the eventtype of 'CTRL + V'.
    Note that now df contains 'from_applicationname'
    which will contain the pair of the last copied/cut applicationname
    """
    paste_events = df[
        (df["eventtype"] == "CTRL + V") & (df["from_applicationname"].notna())
    ]

    """
    Group paste_events by from_applicationname and applicationname and perform count aggregation
    """
    counts = (
        paste_events.groupby(["from_applicationname", "applicationname"])
        .size()
        .reset_index(name="count")
    )
    counts = counts.rename(
        columns={"from_applicationname": "from", "applicationname": "to"}
    )

    return counts.to_dict("records")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
