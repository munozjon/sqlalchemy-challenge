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



#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """Listing available api routes."""
    return (
        f"Here are all available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    recent_dt = dt.datetime.strptime(recent_date.date, "%Y-%m-%d")
    earliest_month = recent_dt - dt.timedelta(days=366)

    last_months = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= earliest_month).all()
    
    session.close()

    latest_prcp = []
    for date, prcp in last_months:
        prcp_dict = {}
        prcp_dict[date] = prcp
        latest_prcp.append(prcp_dict)
    
    return jsonify(latest_prcp)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.name).all()

    session.close()

    stations_list = list(np.ravel(stations))

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():

    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    recent_dt = dt.datetime.strptime(recent_date.date, "%Y-%m-%d")
    earliest_month = recent_dt - dt.timedelta(days=366)


    active_station = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()
    active_station_id = active_station[0]
    last_months_temp = session.query(measurement.tobs).\
        filter(measurement.date >= earliest_month).\
            filter(measurement.station == active_station_id).all()
    
    session.close()

    tobs = [i[0] for i in last_months_temp]

    return jsonify(tobs)


@app.route("/api/v1.0/<start>")
def specific_start(start):
    recent_dt = dt.datetime.strptime(start, "%Y-%m-%d")

    station_stats = session.query(func.min(measurement.tobs), func.max(measurement.tobs),\
                              func.avg(measurement.tobs)).\
                                filter(measurement.date >= recent_dt).all()
    
    session.close()

    stats_list = list(np.ravel(station_stats))

    return stats_list


@app.route("/api/v1.0/<start>/<end>")
def specific_start_end(start, end):
    start_dt = dt.datetime.strptime(start, "%Y-%m-%d")
    end_dt = dt.datetime.strptime(end, "%Y-%m-%d")


    station_stats = session.query(func.min(measurement.tobs), func.max(measurement.tobs),\
                              func.avg(measurement.tobs)).\
                                filter(measurement.date >= start_dt).\
                                    filter(measurement.date <= end_dt).all()
    
    session.close()

    stats_list = list(np.ravel(station_stats))

    return stats_list


if __name__ == '__main__':
    app.run(debug=True)

