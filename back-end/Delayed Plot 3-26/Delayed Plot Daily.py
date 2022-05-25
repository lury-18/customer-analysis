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

# Get daily delays
time_list = []
delay_list = []

# Year 2016
for i in range(10,13):
    for j in range(1,calendar.monthrange(2016, i)[1]+1):
        current = "2016-" + str(i) + "-" + str(j)
        stmt2 = select(func.count()).\
            where(orders.c.delivered_customer > current).\
            where(orders.c.estimated_delivery < current)

        with w_engine.connect() as con:
            d2 = con.execute(stmt2)

        s2 = d2.fetchall()
        time_list.append("2016-" + str(i) + "-" + str(j))
        delay_list.append(s2[0][0])

# Year 2017
for i in range(1,13):
    for j in range(1,calendar.monthrange(2017, i)[1]+1):
        current = "2017-" + str(i) + "-" + str(j)
        stmt2 = select(func.count()).\
            where(orders.c.delivered_customer > current).\
            where(orders.c.estimated_delivery < current)

        with w_engine.connect() as con:
            d2 = con.execute(stmt2)

        s2 = d2.fetchall()
        time_list.append("2017-" + str(i) + "-" + str(j))
        delay_list.append(s2[0][0])

# Year 2018
for i in range(1,9):
    for j in range(1,calendar.monthrange(2018, i)[1]+1):
        current = "2018-" + str(i) + "-" + str(j)
        stmt2 = select(func.count()).\
            where(orders.c.delivered_customer > current).\
            where(orders.c.estimated_delivery < current)

        with w_engine.connect() as con:
            d2 = con.execute(stmt2)

        s2 = d2.fetchall()
        time_list.append("2018-" + str(i) + "-" + str(j))
        delay_list.append(s2[0][0])

app = Flask(__name__)

# Delay data
# This API should return a dictionary of time & delays in each month from "2016-10-01" to "2018-8-31"
# Can consider using this data to create a plot using plotly in dash/shiny
@app.route("/delayplotdata", methods=["GET"])
def delay_plot_data():
    dic = {"time_list":time_list, "delay_list":delay_list}

    return dic