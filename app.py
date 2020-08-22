import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd

from flask import Flask, jsonify
import datetime as dt


app = Flask(__name__)



@app.route("/")
def welcome():
    return(
        "<br/>"
        f"Hello.  Welcome.<br/>"
        "<br/>"
        f"Routes:<br/>"
        "<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date_12-12-2016<br/>"
        f"/api/v1.0/start_12-24-16/end_1-2-17"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    measurement = Base.classes.measurement
    station = Base.classes.station
    session = Session(engine)

    year_ago = dt.datetime(2016, 8, 23)
    results = session.query(measurement.prcp, measurement.date, measurement.station).\
    filter(measurement.date > year_ago).all()
    prcps0 = pd.DataFrame(results)
    prcps = prcps0.iloc[1875:2224]
    prcps.sort_values(by=['date'], inplace=True)
    prcps1 = prcps.set_index('date')
    prcps2 = prcps1.dropna()

    cipitation = prcps2['prcp'].to_dict()
    return jsonify(cipitation)         

@app.route("/api/v1.0/stations")
def stations():
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    measurement = Base.classes.measurement
    station = Base.classes.station
    session = Session(engine)  

    results = session.query(station.station).all()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    measurement = Base.classes.measurement
    station = Base.classes.station
    session = Session(engine)

    year_ago = dt.datetime(2016, 8, 23)
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > year_ago).\
    filter(measurement.station == 'USC00519281').all()

    return jsonify(results)

@app.route("/api/v1.0/start_date_12-12-2016")
def start():
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    measurement = Base.classes.measurement
    station = Base.classes.station
    session = Session(engine)

    start_date = dt.datetime(2016, 12, 12)
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > start_date).all()

    return(
        jsonify(results)   
    )
    

@app.route("/api/v1.0/start_12-24-16/end_1-2-17")
def start_end():   
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    measurement = Base.classes.measurement
    station = Base.classes.station
    session = Session(engine)

    start_date = dt.datetime(2016, 12, 24)
    end_date = dt.datetime(2017, 1, 2)
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > start_date).\
    filter(measurement.date < end_date).all()

    return(
        jsonify(results)   
    )    





if __name__ == "__main__":
    app.run(debug=True)