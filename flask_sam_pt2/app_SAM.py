# Import the dependencies.
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
import numpy as np

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
sql = SQLHelper()


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcom():
    f"Welcome to the Hawaii Climate Analysis API!<br/>"
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/temp/2016-08-23<br/>"
    f"/api?v1.0/temp/2016-08-23/2016-12-31<br/>"


@app.route("/api/v1.0/precipitation")
def precipitation():
    #return the precipitation data for last year
    #calc the date 1 year ago from last database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #query for the precipitation from last year
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    session.close()
    precip = [(date, prep) for date, prep in precipitation]
    return jsonify(precip)

@app.route("/api.v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/2016-08-23<br/>")
def tobs_start(start):
    data = sql.query_tobs_start(start)
    return (data)
@app.route("/api?v1.0/temp/2016-08-23/2016-12-31<br/>")


if __name__ == '__main__':
    app.run(debug=True)