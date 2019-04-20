from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
      "Let's plan a vacation to Hawaii <br/>"
      "<br/>"
      "Below are the available route on this page <br/>"
      "<br/>"
      "/api/precipitation <br/>"  
      "/api/stations <br/>"
      f"/api/start <br/>"
      f"/api/start-end" 
    )

@app.route("/api/v1.0/precipitation")
def last_12_mth_prcp():
    # Calculate the date 2 year ago from today
    last_to_last_yr = dt.date.today() - dt.timedelta(days=2*365)

    # Perform a query to retrieve the data and precipitation scores
    result = session.query(Measurement.date, func.sum(Measurement.prcp).label("prcp")).filter(Measurement.date>last_to_last_yr).\
                group_by(Measurement.date).order_by(Measurement.date).all()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    all_station_prcp = []
    
    for row in result:
        row_dict = {}
        row_dict["date"] = row.date
        row_dict["precipitation"] = row.prcp
        all_station_prcp.append(row_dict)

    return jsonify(all_station_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all stations
    st_results = session.query((func.distinct(Measurement.station).label("station"))).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_names = list(np.ravel(st_results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def temp_obs():
    """Return a list of temperature observation in the station with highest number of observations"""
    # Calculate the date 2 year ago from today
    last_to_last_yr = dt.date.today() - dt.timedelta(days=2*365)
    # Query for USC00519281: station with highest observations
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>last_to_last_yr).\
                filter(Measurement.station == "USC00519281").all()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    all_temp_obs = []
    
    for row in tobs_results:
        row_dict = {}
        row_dict["date"] = row.date
        row_dict["temperture observation"] = row.tobs
        all_temp_obs.append(row_dict)

    return jsonify(all_temp_obs)

@app.route("/api/v1.0/<start_date>")
def temp_info(start_date):
    """Return minimum, maximum and average temperature for all date higher than start date"""
    temp_info = session.query(func.min(Measurement.tobs).label("TMIN"),func.max(Measurement.tobs).label("TMAX"),\
                    func.avg(Measurement.tobs).label("TAVG")).filter(Measurement.date>=start_date).all()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    all_temp_info = []
    
    for row in temp_info:
        row_dict = {}
        row_dict["minimum temperature"] = row.TMIN
        row_dict["maximum temperature"] = row.TMAX
        row_dict["average temperature"] = row.TAVG
        all_temp_info.append(row_dict)

    return jsonify(all_temp_info)

@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_info2(start_date,end_date):
    """Return minimum, maximum and average temperature for all date higher than start date and lower than end date"""
    temp_info = session.query(func.min(Measurement.tobs).label("TMIN"),func.max(Measurement.tobs).label("TMAX"),\
                    func.avg(Measurement.tobs).label("TAVG")).filter(Measurement.date>=start_date).\
                    filter(Measurement.date<=end_date).all()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    all_temp_info = []
    
    for row in temp_info:
        row_dict = {}
        row_dict["minimum temperature"] = row.TMIN
        row_dict["maximum temperature"] = row.TMAX
        row_dict["average temperature"] = row.TAVG
        all_temp_info.append(row_dict)

    return jsonify(all_temp_info)

if __name__ == '__main__':
    app.run(debug=True)