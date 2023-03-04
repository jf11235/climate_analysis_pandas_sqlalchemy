#import flask 
from flask import Flask, jsonify


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(autoload_with=engine)






Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)


#starting at the home page and listing all routes that are available
@app.route("/")

def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"-----to search for dates, enter date as MMDDYYYY------<br/>"
        f"/api/v1.0/start<start><br/>"
        f"/api/v1.0/start<start>/end<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation_funct():
    session = Session(engine)
    #Convert the last_year_prcp query results to a dictionary using date as the key and prcp as the value.
    last_year_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    last_year_prcp = dict(last_year_prcp)
    session.close()
    #Return the JSON representation of your dictionary
    return jsonify(last_year_prcp)
    
    
@app.route("/api/v1.0/stations")
def stations_funct():
    session = Session(engine)
    #Return a JSON list of stations from the dataset.
    stations_list = session.query(Station.station).all()
    stations_list = list(np.ravel(stations_list))
    session.close()
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs_funct():
    session = Session(engine)
    #Return a JSON list of Temperature Observations (tobs) for the previous year
    tobs_list = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
    tobs_list = list(np.ravel(tobs_list))
    session.close()
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_funct(start=None):
    session = Session(engine)
    start_date = dt.datetime.strptime(start, "%m%d%Y")
    #Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    list1 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()
    list1 = list(np.ravel(list1))
    return jsonify(list1)

#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
@app.route("/api/v1.0/<start>/<end>")
def start_end_funct(start, end):
    session = Session(engine)
    start_date = dt.datetime.strptime(start, "%m%d%Y")
    end_date = dt.datetime.strptime(end, "%m%d%Y")
    list2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    list2 = list(np.ravel(list2))
    return jsonify(list2)

if __name__ == "__main__":
    app.run(debug=True)