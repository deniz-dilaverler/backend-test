import datetime
from flask import Flask,jsonify
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from sqlalchemy.orm import   MappedColumn, mapped_column
from sqlalchemy import  BigInteger, ForeignKey 
import pandas as pd

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdata.db'
db = SQLAlchemy(app)


#### SPACE FOR DATABASE STUFF ####

@dataclass
class AppLog(db.Model):
    __tablename__ = 'applog'

    id :MappedColumn[int]= mapped_column(BigInteger, primary_key=True)
    timestarted :MappedColumn[datetime.datetime] = mapped_column()
    timeended :MappedColumn[datetime.datetime]= mapped_column()
    userid :MappedColumn[str]= mapped_column()
    applicationname :MappedColumn[str]= mapped_column()
    windowtitle:MappedColumn[str] = mapped_column()


@dataclass
class UILog(db.Model):
    __tablename__ = 'uilog'

    id : MappedColumn[int] = mapped_column(BigInteger, primary_key=True)
    userid: MappedColumn[str] = mapped_column()
    appid: MappedColumn[int] = mapped_column(BigInteger, ForeignKey("applog.id"))
    eventtype:MappedColumn[str] = mapped_column()
    name :MappedColumn[str]= mapped_column()
    acceleratorkey: MappedColumn[str] = mapped_column()
    timestamp: MappedColumn[datetime.datetime] = mapped_column()


#### SPACE FOR API ENDPOINTS ####


@app.route('/')
def index():
    return {"message": "Hello, World!"}

@app.route('/copyPasteAnalysis')
def copyPasteAnalysis():

    uilog_df = pd.read_sql_query("SELECT u.*, a.applicationname FROM uilog u JOIN applog a ON u.appid = a.id;", db.engine)
    uilog_df["timestamp"] = pd.to_datetime(uilog_df["timestamp"])
    uilog_cp = uilog_df[(uilog_df["eventtype"] == "CTRL + C") |
                        (uilog_df["eventtype"] == "CTRL + X" )|
                        ((uilog_df["eventtype"] == "Left-Down") &  (uilog_df["acceleratorkey"]=="STRG+C" ))
    ]

    uilog_pst = uilog_df[uilog_df["eventtype"] == "CTRL + V"]
    
    uilog_merged = pd.merge_asof(
        left=uilog_pst.sort_values("timestamp"),
        right=uilog_cp.sort_values("timestamp"),
        by="userid",
        direction="backward",
        left_on="timestamp",
        right_on="timestamp"
    )

    uilog_merged = uilog_merged.groupby(["applicationname_x", "applicationname_y"]).size().reset_index(name="count")
    result = uilog_merged.rename(columns={"applicationname_x": "to", "applicationname_y": "from"})

    # Return the data as a JSON response
    return jsonify(result.to_dict("records"))
    
if __name__ == "__main__":
    app.run(debug=True)
