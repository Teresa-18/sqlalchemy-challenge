import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Users/tmlun/sqlalchemy-challenge/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation values"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    session.close()

    # Convert list of tuples into normal list
    #precipitation = list(np.ravel(precipitation))

    return jsonify(precipitation)



@app.route("/api/v1.0/stations")
def stations():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    station = list(np.ravel(results))

    return jsonify(station)


@app.route("/api/v1.0/tobs")
def tobs():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temperature values"""
    # Query all temps from the last year for the station with the most activity
    results = session.query(Measurement.tobs, Measurement.station, Measurement.date).filter(Measurement.station == "USC00519281").filter(func.strftime("%Y-%m-%d",Measurement.date) >= dt.date(2016, 8, 18)).all()

    session.close()

    # Convert list of tuples into normal list
    temperature = list(np.ravel(results))

    return jsonify(temperature)


@app.route("/api/v1.0/<start>")
def temperature_by_start_date():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temperature values"""
    # Query all temp values
    results = session.query(Measurement.tobs, Measurement.date)

    Temp = []
    for date, tobs in results:
        Temp_dict = {}
        Temp_dict["date"] = date
        Temp_dict["temp"] = tobs
        Temp.append(Temp_dict)

    session.close()

    canonicalized = filter(func.strftime("%Y-%m-%d",Measurement.date) >= date.replace("%Y-%m-%d")
    for date in Temp:
        search_term = date["date"].replace("%Y-%m-%d").lower()

        if search_term == canonicalized:
            return jsonify(date)

    return jsonify({"error": "Character not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)
