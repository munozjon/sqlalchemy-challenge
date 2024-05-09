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
    


if __name__ == '__main__':
    app.run(debug=True)

