from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# Calculate the date 1 year ago from the last data point in the database
prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
prev_year


#################################################
# Flask Routes
#################################################

@app.route("/")
def justice_league():
    """Return the justice league data as json"""

    return jsonify(justice_league_members)


@app.route("/")
def welcome():
    """ List of available API"""
    return (
        
        f"Welcome to Hawai APi<br/>"        
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>
        f"/api/v1.0/<start>/<end><br/>
    )
        
 
@app.route("/api/v1.0/precipitation<br/>")
def precipitation(real_name):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = real_name.replace(" ", "").lower()
    for character in justice_league_members:
        search_term = character["real_name"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(character)

    return jsonify({"error": f"Character with real_name {real_name} not found."}), 404

#Return a JSON list of stations from the dataset.
@app.route("api/v1.0/stations<br/>")
def stations():
    unique_stations = session.query(Measurement.station).distinct().all()
    return jsonify(unique_stations)

@app.route("/api/v1.0/tobs<br/>")
def temperature_observations():
    """
     query for the dates and temperature observations from a year from the last data point.
     """
     temperature_tobs = session.query(Measurements.tobs).\
        filter(Measurement.tobs > prev_year).\
        all()
    return jsonify(temperature_tobs)


    

    


if __name__ == "__main__":
    app.run(debug=True)
