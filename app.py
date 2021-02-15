    # import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, and_, or_, not_, desc
import os

# N.B. external config.py file should be formatted like:
# login = 'postgres:password' where password is set to whatever your database password is. Default username is 
# postgres, but change this if you use a different username.
# import psycopg2


#################################################
# Deploy to Heroku
#################################################

postgres_str = os.environ.get('DATABASE_URL', '')

#################################################
# Otherwise not
#################################################



app.debug = True
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
    # Create the connection
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_str
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
Historic = Base.classes.historic

from sqlalchemy import select, insert
select_stmt = select([Predicted_values])

data = connection.execute(select_stmt).fetchall()




# create route that renders index.html template
@app.route("/")
def home():

    return render_template("index.html", data=data)

@app.route("/previous")
def previous():
    select_stmt_2nd = select([Historic])
    data3 = connection.execute(select_stmt_2nd).fetchall()

    return render_template("previous.html", data3=data3)



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


