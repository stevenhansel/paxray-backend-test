import os
from dataclasses import dataclass
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship
import pandas as pd

basedir = os.path.abspath(os.path.dirname(__file__))
sqlitedir = f"sqlite:///{os.path.join(basedir, 'testdata.db')}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = sqlitedir

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

    return countCopyPasteEvents(data)


def countCopyPasteEvents(data):
    df = pd.DataFrame(data)

    """
    Add another auxiliary column 'fromApplicationname',
    to prefill the application name of the last copied/cut eventtype into all of the rows
    """
    df_copying_filter = df["eventtype"].isin(["CTRL + C", "CTRL + X"]) | (
        (df["eventtype"] == "Left-Down") & (df["acceleratorkey"] == "STRG+C")
    )

    df["fromApplicationname"] = (
        df["applicationname"].where(df_copying_filter).groupby(df["userid"]).ffill()
    )

    """
    Flag whether a new copying event has occurred on each row of the DataFrame.
    Utilize cumsum (Cumulative Sum) to create an identifier for
    a segment of each copy/paste action
    """
    df["isCopying"] = df_copying_filter
    df["groupid"] = df["isCopying"].cumsum()

    """
    Filter such that df only contains the eventtype of 'CTRL + V'.
    Note that now df contains 'fromApplicationname'
    which will contain the pair of the last copied/cut applicationname
    """
    df_transitions = df[
        (df["eventtype"] == "CTRL + V") & (df["fromApplicationname"].notna())
    ]

    """
    If there are duplicates in a segment, particularly by the
    groupid (cumulative sum throughout `isCopying`), then drop the duplicates.
    """
    df_transitions = df_transitions.drop_duplicates(
        subset=["groupid", "userid", "fromApplicationname", "applicationname"]
    )

    """
    Group paste_events by fromApplicationname and applicationname,
    then perform count aggregation
    """
    counts = (
        df_transitions.groupby(["fromApplicationname", "applicationname"])
        .size()
        .reset_index(name="count")
    )
    counts = counts.rename(
        columns={"fromApplicationname": "from", "applicationname": "to"}
    )

    return counts.to_dict("records")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
