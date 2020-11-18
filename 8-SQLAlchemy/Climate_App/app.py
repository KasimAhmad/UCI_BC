import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify
#----------------------------------------------------------------------
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
#----------------------------------------------------------------------
Measurements = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#----------------------------------------------------------------------
app = Flask(__name__)
#----------------------------------------------------------------------
@app.route("/")
def intro():
    return (
        f"Welcome to the Climate API!<br/> "
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Last year's rain totals from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"List of Stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Last year's temperatures from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/startdate(YYYY-MM-DD) & calculates the AVG/MAX/MIN temp for start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"/api/v1.0/startdate(YYYY-MM-DD)/enddate(YYYY-MM-DD) & calculates the AVG/MAX/MIN temp in between start and end dates<br/>"
    )
#----------------------------------------------------------------------
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    recent = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    past_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_data = session.query(Measurements.date, Measurements.prcp).\
            filter(Measurements.date > past_year).\
            order_by(Measurements.date).all()
    session.close()

    prcp_total = []
    for result in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = prcp_data[0]
        prcp_dict["prcp"] = prcp_data[1]
        prcp_total.append(prcp_dict)
    return jsonify(prcp_total)
#----------------------------------------------------------------------
@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())
#----------------------------------------------------------------------
@app.route("/api/v1.0/tobs")
def tobs():
    
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature = session.query(Measurements.date, Measurements.tobs).\
        filter(Measurements.date > last_year).\
        order_by(Measurements.date).all()

    temp_total = []
    for result in temperature:
        tobs_dict = {}
        tobs_dict["date"] = temperature[0]
        tobs_dict["tobs"] = temperature[1]
        temp_total.append(tobs_dict)
    return jsonify(temp_total)
#----------------------------------------------------------------------
@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start_dt).all()
    session.close()
    to_list = []
    for result in results:
        r = {}
        r["StartDate"] = start_dt
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        to_list.append(r)
    return jsonify(to_list)
#----------------------------------------------------------------------
@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start,end):

    session = Session(engine)
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    end_dt = dt.datetime.strptime(end, "%Y-%m-%d")
    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start_dt).filter(Measurements.date <= end_dt)
    session.close()
    to_list = []
    for result in results:
        r = {}
        r["StartDate"] = start_dt
        r["EndDate"] = end_dt
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        to_list.append(r)
    return jsonify(to_list)
#----------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)