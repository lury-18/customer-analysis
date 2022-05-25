from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import joblib
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine, inspect, select, text, and_, or_, func
from sqlalchemy import Table, MetaData
from datetime import datetime

import json

# Connect to database
passwd = 'FyZSMAiH'
w_engine = create_engine('mysql+pymysql://e0376935:' + passwd + '@localhost:3306/olist', echo=True)

m2 = MetaData(bind=w_engine)
m2.reflect()

orders = Table("orders", m2, autoload=True)

def select_orders(start_time, end_time, status):
    start_datetime = datetime.strptime(start_time, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_time, '%Y-%m-%d')

    query1 = select([orders]).\
        where(orders.c.order_status == status).\
        where(orders.c.purchase_time > start_datetime).\
        where(orders.c.purchase_time < end_datetime).\
        order_by(orders.c.purchase_time).limit(1)
    
    with w_engine.connect() as con:
        d1 = con.execute(query1)
    
    return d1.fetchall()



app = Flask(__name__)

# Order Filter
# This API should return a list containing orders from one time to another
# "status" argument determines the order is "delievered" ot "cancelled" etc.
@app.route("/orders", methods=["GET"])
def order_filter():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    status = request.args.get('status')

    s1 = select_orders(start_time, end_time, status)

    c1,c2,c3,c4,c5,c6,c7,c8 = [],[],[],[],[],[],[],[]

    for i in range(len(s1)):
        c1.append(s1[i][0])
        c2.append(s1[i][1])
        c3.append(s1[i][2])
        c4.append(s1[i][3])
        c5.append(s1[i][4])
        c6.append(s1[i][5])
        c7.append(s1[i][6])
        c8.append(s1[i][7])

    dic = {"order_id":c1,"customer_id":c2,"order_status":c3,"purchase_time":c4,"approval_time":c5,
    "delivered_carrier":c6,"delivered_customer":c7,"estimated_delivery":c8}

    return dic


