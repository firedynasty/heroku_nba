    # import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import pandas as pd

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, and_, or_, not_, desc

# N.B. external config.py file should be formatted like:
# login = 'postgres:password' where password is set to whatever your database password is. Default username is 
# postgres, but change this if you use a different username.
import psycopg2
postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'
                .format(username='postgres',
                        password='postgres',
                        ipaddress='localhost',
                        port=5432,
                        dbname='flask_deploy'))

# postgres_str = app.config['SQL_ALCHEMY_DATABASE_URI'] = 'postgres://umydthrhevlwbv:a166611fc4fda747769900bb51cfb8cbd633cebe3ec13fdfc2180772a9d3bc8d@ec2-18-204-101-137.compute-1.amazonaws.com:5432/d9ugm948kmolua'


app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_str
    # Create the connection
engine = create_engine(postgres_str)
connection = engine.connect()
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
    # app.debug = False



db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(engine, reflect=True)
Predicted_values = Base.classes.predicted_values
Box_scores = Base.classes.box_score_2021


from sqlalchemy import select, insert
select_stmt = select([Predicted_values])

data = connection.execute(select_stmt).fetchall()


# create route that renders index.html template
@app.route("/")
def home():

    return render_template("index.html", data=data)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        book = request.form['book']
        book1 = str(book)
        # search by author or book
        select_stmt3 = select([Box_scores]).where(Box_scores.HOME_ABBR == book1)
        select_stmt3 = select_stmt3.order_by(Box_scores.DATE)

        data2 = connection.execute(select_stmt3).fetchall()

        return render_template('index.html', data=data, data2=data2)
    return render_template('search.html')

@app.route('/addition')

def additon():
    select_stmt2 = select([Pets])
    data1 = connection.execute(select_stmt2).fetchall()
    return render_template("index.html", data=data1)





if __name__ == "__main__":
    app.debug = True
    app.run()


