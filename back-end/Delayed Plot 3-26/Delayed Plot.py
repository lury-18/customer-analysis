# Set-Ups 
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import joblib
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine, inspect, select, text, and_, or_, func
from sqlalchemy import Table, MetaData

from datetime import datetime
import calendar

import json
import matplotlib.pyplot as plt

# Connect to database
passwd = 'FyZSMAiH'
w_engine = create_engine('mysql+pymysql://e0376935:' + passwd + '@localhost:3306/olist', echo=True)

m2 = MetaData(bind=w_engine)
m2.reflect()

orders = Table("orders", m2, autoload=True)

# Get monthly delays
time_list = []
delay_list = []

# Year 2016
for i in range(10,13):
    day1 = "2016-" + str(i) + "-01" 
    day31 = "2016-" + str(i) + "-" + str(calendar.monthrange(2016, i)[1])

    stmt2 = select(func.count()).\
        where(orders.c.delivered_customer > orders.c.estimated_delivery).\
        where(orders.c.delivered_customer > day1).\
        where(orders.c.estimated_delivery < day31)
    
    with w_engine.connect() as con:
        d2 = con.execute(stmt2)
    
    s2 = d2.fetchall()

    time_list.append("2016-" + str(i))
    delay_list.append(s2[0][0])


# Year 2017
for i in range(1,13):
    day1 = "2017-" + str(i)  + "-01" 
    day31 = "2017-" + str(i) + "-" + str(calendar.monthrange(2017, i)[1])

    stmt2 = select(func.count()).\
        where(orders.c.delivered_customer > orders.c.estimated_delivery).\
        where(orders.c.delivered_customer > day1).\
        where(orders.c.estimated_delivery < day31)
    
    with w_engine.connect() as con:
        d2 = con.execute(stmt2)
    
    s2 = d2.fetchall()

    time_list.append("2017-" + str(i))
    delay_list.append(s2[0][0])


# Year 2018
for i in range(1,9):
    day1 = "2018-" + str(i)  + "-01" 
    day31 = "2018-" + str(i) + "-" + str(calendar.monthrange(2018, i)[1])

    stmt2 = select(func.count()).\
        where(orders.c.delivered_customer > orders.c.estimated_delivery).\
        where(orders.c.delivered_customer > day1).\
        where(orders.c.estimated_delivery < day31)
    
    with w_engine.connect() as con:
        d2 = con.execute(stmt2)
    
    s2 = d2.fetchall()

    time_list.append("2018-" + str(i))
    delay_list.append(s2[0][0])


app = Flask(__name__)

# Delay Plot
# This API should return a plot for delays from one month to another
# time args can only in range "2016-10" to "2018-8"
@app.route("/delayplot", methods=["GET"])
def delay_plot():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if (start_time not in time_list) or (end_time not in time_list):
        return "Please check your input! Remember to type 2017-5 instead of 2017-05!"
    
    i1 = time_list.index(start_time)
    i2 = time_list.index(end_time)

    plt.plot(time_list[i1:i2+1],delay_list[i1:i2+1])
    plt.savefig("plot1.png")

    return send_file("plot1.png")

# Delay Plot
# This API should return a dictionary of time & delays in each month from "2016-10" to "2018-8"
# Can consider using this data to create a plot using plotly in dash/shiny
@app.route("/delayplotdata", methods=["GET"])
def delay_plot_data():
    dic = {"time_list":time_list, "delay_list":delay_list}

    return dic
