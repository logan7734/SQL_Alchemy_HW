#Importing a lof of dependencies

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Setting up the DB
#Connecting to DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)


#Reference to tables in DB
Station = Base.classes.station
Measurement = Base.classes.measurement

#Initiate session

session = Session(engine)

#Bring in Flask
app = Flask(__name__)

#Declare the route
@app.route("/")

def welcome():
    """Welcome! Below are a list of all available API Routes."""
    
    return (
            
            f"Welcome to the Surfs Up API.<br>"
            f"Available routes below:<br>"
            f"/api/precipitation<br>"
            f"/api/stations<br>"
            f"/api/temperature<br>"
    )

#Declare the route
@app.route("/api/precipitation")

def precipitation():
    """Function that returns data of rainfall in Hawaii for the last year."""

    #Get the latest date in DB
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #query date
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    #query
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
                   filter(Measurement.date >= query_date).\
                   order_by(Measurement.date).all()


    #Create list of dictionaries; (Keys: 'date', Values: 'prcp')
    prcp_list = []
    #loop through the query to get data and save it in prcp_list
    for item in precip_query:
        prcp_dict = {}
        prcp_dict["date"] = item[0]
        prcp_dict["prcp"] = item[1]
        prcp_list.append(prcp_dict)

    #Return jsonified prcp_list
    return jsonify(prcp_list)


#Declare the route
@app.route("/api/stations")

#Function definition: 'stations'

def stations():
    """API Route Function that returns a list of stations from data-set."""

    #Get stations from DB
    stations_query = session.query(Station.name, Station.station)
    stations_pd = pd.read_sql(stations_query.statement, stations_query.session.bind)
    #return jsonified dict of stations_pd
    return jsonify(stations_pd.to_dict())


#Declare the route
@app.route("/api/temperature")

#Function definition: 'temperature'
def temperature():
    """API Route Function that returns a list of Temperature observations(tobs) for the previous year."""

    #Get the latest date in DB
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #query date
    query_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    #build query for temperature of last year
    temp_query = session.query(Measurement.date, Measurement.tobs).\
                 filter(Measurement.date >= query_year).\
                 order_by(Measurement.date).all()

    #Create a list of dictionaries; (Keys: "date", Values: "temperature")
    temperatures = []

    #loop through query object: temp_query
    for temp in temp_query:
        temp_data = {}
        temp_data["date"] = temp[0]
        temp_data["tobs"] = temp[1]
        temperatures.append(temp_data)

    #Return jsonified 'temperatures' list
    return jsonify(temperatures)



if __name__ == '__main__':
    app.run(debug=True)