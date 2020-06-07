import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from src.create_db import Price_Prediction
from flask_sqlalchemy import SQLAlchemy
import pickle
import pandas as pd


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

# read in dataframe 
data = pd.read_csv("data/features.csv") 

# load the model for prediction
model = pickle.load(open(app.config['SAVE_TMO_PATH'], 'rb'))

# Initialize the database
db = SQLAlchemy(app)
print(db)


def clean_input(state, region_input, housing_type, sqfeet, beds, baths, comes_furnished_input, 
    laundry_options, smoking_allowed_input, dogs_allowed_input, wheelchair_access_input):

    sqfeet = int(sqfeet)
    beds = int(beds)
    baths = float(baths)

    # create indicator variable for high-price-region
    region = 0 if region_input=='Others' else 1

    # transform binary categorical variables from Yes/No to 1/0
    comes_furnished = 1 if comes_furnished_input=='Yes' else 0
    smoking_allowed = 1 if smoking_allowed_input=='Yes' else 0
    dogs_allowed = 1 if dogs_allowed_input=='Yes' else 0
    wheelchair_access = 1 if wheelchair_access_input=='Yes' else 0

    input_ls = [state, region, housing_type, sqfeet, beds, baths, comes_furnished, \
                laundry_options, smoking_allowed, dogs_allowed, wheelchair_access]

    return input_ls


def prediction(input_ls):

    state = input_ls[0]
    region = input_ls[1]
    housing_type = input_ls[2]
    sqfeet = input_ls[3]
    beds = input_ls[4]
    baths = input_ls[5]
    comes_furnished = input_ls[6]
    laundry_options = input_ls[7]
    smoking_allowed = input_ls[8]
    dogs_allowed = input_ls[9]
    wheelchair_access = input_ls[10]

    # create a dataframe to store inputs for prediction
    df = pd.DataFrame(columns=list(data.columns)[1:])

    ls = [sqfeet, beds, baths, smoking_allowed, dogs_allowed, wheelchair_access, comes_furnished]
    for i in range(67):
        ls.append(0)
    df.loc[0] = ls

    type_col = 'type_' + housing_type
    laundry_options_col = 'laundry_options_' + laundry_options
    state_col = 'state_' + state

    df[type_col] = 1
    df[laundry_options_col] = 1
    df[state_col] = 1
    df['high_price_region'] = region

    # make prediction
    pred_price = int(model.predict(df)[0])

    return pred_price


@app.route('/')
def index():
    """Main view of the web page

    Returns: 
        rendered html template
    """

    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with housing features input from user

    Returns: 
        rendered html template
    """

    # clean user input
    input_ls = clean_input(request.form['state'], request.form['region'], request.form['type'], request.form['sqfeet'],
                           request.form['beds'], request.form['baths'], request.form['comes_furnished'], 
                           request.form['laundry_options'], request.form['smoking_allowed'], request.form['dogs_allowed'],
                           request.form['wheelchair_access'])

    # get prediction
    pred_price = prediction(input_ls)
    result = "$" + str(pred_price)


    # # get feature value from user input
    # state = request.form['state']
    # region_input = request.form['region']
    # housing_type = request.form['type']
    # sqfeet = int(request.form['sqfeet'])
    # beds = int(request.form['beds'])
    # baths = float(request.form['baths'])
    # comes_furnished_input = request.form['comes_furnished']
    # laundry_options = request.form['laundry_options']
    # smoking_allowed_input = request.form['smoking_allowed']
    # dogs_allowed_input = request.form['dogs_allowed']
    # wheelchair_access_input = request.form['wheelchair_access']

    # # create indicator variable for high-price-region
    # region = 0 if region_input=='Others' else 1

    # # transform binary categorical variables from Yes/No to 1/0
    # comes_furnished = 1 if comes_furnished_input=='Yes' else 0
    # smoking_allowed = 1 if smoking_allowed_input=='Yes' else 0
    # dogs_allowed = 1 if dogs_allowed_input=='Yes' else 0
    # wheelchair_access = 1 if wheelchair_access_input=='Yes' else 0



    # # create a dataframe to store inputs for prediction
    # df = pd.DataFrame(columns=list(data.columns)[1:])


    # ls = [sqfeet, beds, baths, smoking_allowed, dogs_allowed, wheelchair_access, comes_furnished]
    # for i in range(67):
    #     ls.append(0)
    # df.loc[0] = ls

    # type_col = 'type_' + housing_type
    # laundry_options_col = 'laundry_options_' + laundry_options
    # state_col = 'state_' + state

    # df[type_col] = 1
    # df[laundry_options_col] = 1
    # df[state_col] = 1
    # df['high_price_region'] = region


    # make prediction
    #pred_price = int(model.predict(df)[0])
    #return render_template('index.html', result=result)


    try:
        user_input = Price_Prediction(state=input_ls[0],
                                      region=input_ls[1],
                                      housing_type=input_ls[2], 
                                      sqfeet=input_ls[3], 
                                      beds=input_ls[4], 
                                      baths=input_ls[5],
                                      comes_furnished=input_ls[6],
                                      laundry_options=input_ls[7],
                                      smoking_allowed=input_ls[8],
                                      dogs_allowed=input_ls[9],
                                      wheelchair_access=input_ls[10],
                                      pred_price=pred_price)
        
        db.session.add(user_input)
        db.session.commit()
        logger.info("USA Housing Price Predictor result added: %s", result)
        return render_template('index.html', result=result)
    except:
        #traceback.print_exc()
        logger.warning("Not able to display housing price prediction, error page returned")
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])



