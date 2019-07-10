from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt


# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Calculate the date 1 year ago from the last data point in the database
prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """ List of available API"""
    return (
        
        f"Welcome to Hawai API<br/>"        
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
        
#Convert the query results to a Dictionary using date as the key and prcp as the value.

@app.route("/api/v1.0/precipitation")
def precipitation(): 
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    print(prev_year)
    months_list = session.query(Measurement.date,Measurement.prcp).\
                    filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in months_list}
    print(precip)
    return jsonify(precip)    
    
    
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    unique_stations = session.query(Station.station).all()
    print(unique_stations)
    return jsonify(unique_stations)
                

# #query for the dates and temperature observations from a year from the last data point.
# #Return a JSON list of Temperature Observations (tobs) for the previous year.                   

@app.route("/api/v1.0/tobs")
def temperature_observations():
    temperature_tobs = session.query(Measurement.tobs).\
        filter(Measurement.date > prev_year).\
        all()
    return jsonify(temperature_tobs)
                   
                   
# #/api/v1.0/<start> and /api/v1.0/<start>/<end>
# #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# #When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.              
                   
@app.route("/api/v1.0/<start>")
def stats(start=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    # calculate TMIN, TAVG, TMAX for dates greater than start
    results = session.query(*sel).\
        filter(Measurement.date >= start).all()
    print(results)
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    print(temps)
    return jsonify(temps)


@app.route("/api/v1.0/<start>/<end>")              
def stats_end(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        print(results)
        # Unravel results into a 1D array and convert to a list
        temps = list(np.ravel(results))
        print(temps)
        return jsonify(temps)
    
# calculate TMIN, TAVG, TMAX with start and stop
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    print(results)
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    print(temps)
    return jsonify(temps)



if __name__ == "__main__":
    app.run(debug=True)
