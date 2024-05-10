# Import the dependencies.
import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station

measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(bind=engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# Find the most recent date, and get the earliest date from the year prior
# To be used for '/precipitation' and 'tobs' routes
recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
recent_dt = dt.datetime.strptime(recent_date.date, "%Y-%m-%d")
earliest_dt = recent_dt - dt.timedelta(days=366)

# Function to convert a tuple into a list for queries
def tuple_to_list(tuple):
    return list(np.ravel(tuple))

# Function to convert dynamic routes' start and end dates into datetime
def date_time(date):
    return dt.datetime.strptime(date, "%m%d%Y")



#################################################
# Flask Routes
#################################################

# Homepage route
@app.route("/")
def homepage():

    # Return text to demonstrate the routes
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Here are all available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<br/>"
        f"The 'start' and 'end' dates should be in the following format: MMDDYYYY"
    )

# should just be a dictionary, do not make it a lsit
# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query the database for dates and precipitation for the last year
    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= earliest_dt).all()
    
    session.close()

    # Create a dictionary with the dates and precipitation as keys and values
    prcp_dict = {}
    for date, prcp in precipitation:
        prcp_dict[date] = prcp
    
    # Return the dictionary with jsonify
    return jsonify(prcp_dict)


# Stations route
@app.route("/api/v1.0/stations")
def stations():

    # Query database for all the station IDs
    stations = session.query(station.station).all()

    session.close()

    # Convert the tuple of station IDs into a list
    stations_list = tuple_to_list(stations)

    # Create dictionary for stations
    stations_dict = {'stations': stations_list}

    # Return the list of station IDs with jsonify
    return jsonify(stations_dict)


# TOBS route
@app.route("/api/v1.0/tobs")
def tobs():

    # Query the database for the station with the most activity
    active_station = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()
    
    # Extract the station's ID
    active_station_id = active_station[0]

    # Query the database for the most active station's tobs data for the last year
    temperatures = session.query(measurement.tobs).\
        filter(measurement.date >= earliest_dt).\
            filter(measurement.station == active_station_id).all()
    
    session.close()

    # Convert the queried data into a list
    tobs = [i[0] for i in temperatures]

    # Create dictionary for the tobs data
    tobs_dict = {'tobs': tobs}

    # Return the dictionary of tobs data with jsonify
    return jsonify(tobs_dict)


# Start date route
@app.route("/api/v1.0/temp/<start>")
def specific_start(start):

    # Convert the start date into datetime
    start_dt = date_time(start)

    # Query the database for the min, max, and average tobs since the provided start date
    station_stats = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),\
                                  func.max(measurement.tobs)).\
                                filter(measurement.date >= start_dt).all()
    
    session.close()

    # Convert tuple of responses into a list
    stats_list = tuple_to_list(station_stats)
    
    # Create dictionary for the responses
    stats_dict = {'temps': stats_list}

    # Return the dictionary
    return stats_dict


# Start/End dates route
@app.route("/api/v1.0/temp/<start>/<end>")
def specific_start_end(start, end):

    # Convert provided start and end dates into datetime
    start_dt = date_time(start)
    end_dt = date_time(end)

    # Query the database for min, max, and avg tobs
    # Filtered for data between the provided start and end dates
    station_stats = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),\
                                  func.max(measurement.tobs)).\
                                filter(measurement.date >= start_dt).\
                                    filter(measurement.date <= end_dt).all()
    
    session.close()

    # Convert response tuple into a list
    stats_list = tuple_to_list(station_stats)

    # Create dictionary for the responses
    stats_dict = {'temps': stats_list}

    # Return the dictionary
    return stats_dict


if __name__ == '__main__':
    app.run(debug=True)

