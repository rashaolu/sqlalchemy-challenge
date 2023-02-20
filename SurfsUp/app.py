import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite") 


# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Flask Setup
app = Flask(__name__)

#Flask Routes
@app.route("/")
def welcome():
    """List all available routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session link
    session=Session(engine) 
    """Return a list of past 12 months of data. """
    #Query 12 months of data
    query_date=dt.date(2017,8,23)-dt.timedelta(days=365)
    scores_date=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=query_date).all()
    
    session.close()

    #convert to a dictionary
    pr=[]
    for date,prcp in scores_date:
        pr_dict={}
        pr_dict["date"]=date
        pr_dict["prcp"]=prcp
        pr.append(pr_dict)
    return jsonify(pr)

@app.route("/api/v1.0/stations")
def stations():
    #create session link
    session=Session(engine)
    """Return list of stations"""
    #Query list of stations and count 
    sel=[Measurement.station,func.count(Measurement.id)]
    active=session.query(*sel).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
    session.close()

    #convert to a list
    station=list(np.ravel(active))
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    #create session link
    session=Session(engine)
    """Return a list of most-active station temp for previous year of data"""
    #query the dates
    query_date=dt.date(2017,8,23)-dt.timedelta(days=365)
    obs=session.query(Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date>=query_date).all()

    session.close()
    # convert to a list
    temp=list(np.ravel(obs))
    return jsonify(temp) 

@app.route("/api/v1.0/start")
def start():
    #create session link 
    session= Session(engine)
    """Returns tmin,tavg,tmax for a specified start date"""
    #query the dates 
    #date=dt.date(2016,11,9)
    sel=[func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    start_date= session.query(*sel, Measurement.date).group_by(Measurement.date).filter(Measurement.date>=dt.date(2016,11,9)).all()

    session.close()
    
    #convert to list
    sd=list(np.ravel(start_date))
    return jsonify(sd)

@app.route("/api/v1.0/start/end")
def end():
    #create session link 
    session= Session(engine)
    """Returns tmin,tavg,tmax for a specified start date"""
    #query the dates 
    sel=[func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    start_end= session.query(*sel, Measurement.date).group_by(Measurement.date).filter(Measurement.date>=dt.date(2016,1,24)).filter(Measurement.date<=dt.date(2017,1,24)).all()

    session.close()
    
    #convert to list
    se=list(np.ravel(start_end))
    return jsonify(se)

if __name__== "__main__":
    app.run(debug=True)

