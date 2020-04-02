import datetime as datetime
import numpy as np 
import pandas as pd


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#jsonify so that it can create a response for non dict
from flask import Flask, jsonify

#just like part 1 of Hw
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base= automap_base()
Base.prepare(engine, reflect=True)

Measurement= Base.classes.measurement
Station= Base.classes.station

session= Session(engine)

#flask app
app= Flask(__name__)

#flask routes

@app.route("/")
def Homepage():
    """List of all routes that are available"""
    return(
        f"/api/v1.0/precipitation"

        f"/api/v1.0/station"

        f"/api/v1.0/tobs"

        f"/api/v1.0/<start>"

        f"/api/v1.0/<start>/<end>"
    )   


#found the dates for the last 12 months in part one of hw
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return list of Last 12 months Precipitation Data"""
    prcp= [Measurement.date, Measurement.prcp]
    result= session.query(*prcp).all()
    session.close()

    precipitation= []
    for date, prcp in result: 
        prcp_dict= {}
        prcp_dict["Date"]= date
        prcp_dict["Precipitation"]= prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/station")
def stations():
    """Return List of Stations"""
    results= session.query(Station.name, Station.station, Station.elevation).all()

    station_list= []
    for result in results: 
        row= {}
        row['name']=result[0]
        row['station']=result[1]
        row['elevation']=result[2]
        station_list.append(row)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp_obs():
    """Return list of temperature observations for the previous year"""
    results= session.query(Station.name, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24", Measurement.date <= "2017-08-23").all()

    tobs_list= []
    for result in results: 
        row= {}
        row["Station"]= result[0]
        row["Date"]= result[1]
        row["Temperature"]= int(result[2])
        tobs_list.append(row)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def tobs_date(start):
    """Return the average temp, max temp, and min temp for the date"""
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

   #couldnt get to not display null values :( tried float but gave me a type error!
    tobs_list = []
    for result in results:
        row = {}
        row['Start Date'] = start
        row['End Date'] = '2017-08-23'
        row['Average Temperature'] = result[0]
        row['Highest Temperature'] = result[1]
        row['Lowest Temperature'] = result[2]
        tobs_list.append(row)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>/<end>")
def dates(start, end):
    """Return the avg, max and min between start and end date"""
    results= session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    data_list= []
    for result in results: 
        row= {}
        row["Start Date"]= start
        row["End Date"]= end
        row["Average Temperature"]= float(result[0])
        row["Highest Temperature"]= float(result[1])
        row["Lowest Temperature"]= float(result[2])
        data_list.append(row)

    return jsonify(data_list)


if __name__ == '__main__':
    app.run(debug=True)