from flask import Flask
import datetime
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from sqlalchemy.orm import   MappedColumn, mapped_column
from sqlalchemy import  BigInteger, ForeignKey 

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
    # TODO
    return {}

    
if __name__ == "__main__":
    app.run(debug=True)
