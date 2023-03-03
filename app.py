#import flask 
from flask import Flask, jsonify
app = Flask(__name__)

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

# reflect the tables
Base.prepare(autoload_with=engine)

# Create our session (link) from Python to the DB
session = Session(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station



#starting at the home page and listing all routes that are available
@app.route("/")

def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"to search for dates, enter date as MMDDYYYY<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation_funct():
    #Convert the last_year_prcp query results to a dictionary using date as the key and prcp as the value.
    last_year_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    
    #Return the JSON representation of your dictionary
    return jsonify(last_year_prcp)
    
    
@app.route("/api/v1.0/stations")
def stations_funct():
    #Return a JSON list of stations from the dataset.
    stations = session.query(Station.station).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs_funct():
    #Return a JSON list of Temperature Observations (tobs) for the previous year
    tobs_list = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()

@app.route("/api/v1.0/<start>")
def start_funct():
    start_date = dt.datetime.strptime('start', '%m%d%Y')
    #Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    list = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    return jsonify(list)

#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
@app.route("/api/v1.0/<start>/<end>")
def start_end_funct(start, end):
    start_date = dt.datetime.strptime(start, '%m%d%Y')
    end_date = dt.datetime.strptime(end, '%m%d%Y')
    list = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(list)