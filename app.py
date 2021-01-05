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
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"**start date should be entered as yyyy-mm-dd**<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"**start and end dates should be entered as yyyy-mm-dd**"
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

    all_stations = session.query((func.count(Measurement.station)), Measurement.station).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    query_date_2 = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    last_year = session.query(Measurement.tobs, Measurement.station, Measurement.date).\
    filter(Measurement.station == all_stations[0][1]).\
    filter(func.strftime("%Y-%m-%d",Measurement.date) >= query_date_2).all()

    session.close()

    # Convert list of tuples into normal list
    temperature = list(np.ravel(last_year))

    return jsonify(temperature)


@app.route("/api/v1.0/<start>")
def temperature_by_start_date(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    ################################################
    # Return a JSON list of the minimum temperature, the average temperature, 
    # and the max temperature for a given start
    ##################################################

    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
filter(Measurement.date >= start).order_by(Measurement.date.desc()).all()

    Temp = []
    for temps in results:
        Temp_dict = {}
        Temp_dict["Minimum Temp"] = results[0][0]
        Temp_dict["Maximum Temp"] = results[0][1]
        Temp_dict["Average Temp"] = results[0][2]
        Temp.append(Temp_dict)

    session.close()

    return jsonify(Temp)

@app.route("/api/v1.0/<start>/<end>")
def temperature_by_start_end(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    ################################################
    # Return a JSON list of the minimum temperature, the average temperature, 
    # and the max temperature for a given start and end date
    ##################################################

    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
filter(Measurement.date >= start, Measurement.date <= end).order_by(Measurement.date.desc()).all()

    Temp2 = []
    for temps in results:
        Temp2_dict = {}
        Temp2_dict["Minimum Temp"] = results[0][0]
        Temp2_dict["Maximum Temp"] = results[0][1]
        Temp2_dict["Average Temp"] = results[0][2]
        Temp2.append(Temp2_dict)

    session.close()

    return jsonify(Temp2)

if __name__ == "__main__":
    app.run(debug=True)
