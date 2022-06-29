from application import app
from flask import render_template, url_for
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import session
from sqlalchemy import create_engine, Table, MetaData
import pandas as pd
import json
import plotly
import plotly_express as px



#Connect to the database in AWS
url = "postgresql://root:root12345@database-165.cdebrk5iwu37.us-east-1.rds.amazonaws.com:5432/postgres"
engine = create_engine(url)
connect = engine.connect()


@app.route('/')
def index():
    # output second pandas dataframe, creating third figure and setting the data to Json
    query2 = '''select month_created,
	                to_char(date_created, 'Month') as Month,
	                count(operation_id) as transaction_qty,
	                round(cast(sum(transaction_amount)/1000 as numeric), 2) as total_cost
                from whole_collection_geom
                where fraud_flag='Yes'
                group by 1,2
                order by 1
                '''
    # output is pandas dataframe
    month_detail = pd.read_sql(query2, con=connect)
    fig3=px.histogram(month_detail,x=month_detail['month_created'],y=month_detail['transaction_qty'], nbins=20,
                  color_discrete_sequence=['indianred'],
                  title='Transacciones fraudulentas por mes',
                  labels={'month_created':'Mes','transaction_qty':'Cantidad de transacciones'},
                  text_auto=True,)
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("index.html", title= "Home", graphJSON3= graphJSON3 )