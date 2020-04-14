# USA Housing Price Predictor App

**Developer**: Yanmeng (Selina) Song    
**QA**: Lirong Ma

<!-- toc -->

- [Project Charter](#project-charter)
- [Backlog](#backlog)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)

<!-- tocstop -->
## Project charter

### Vision: 
Housing price information online is kind of scattered. It takes lots of time and effort to collect such information and then analyze them to evaluate the price of a specific house that fits users’ needs, especially when it comes to the US states as a whole instead of isolated urban housing markets. 

This project is born in order to: 1) enable potential homebuyers to efficiently find the up-to-date countrywide housing price information based on their preferences, 2) help house sellers better understand the housing market before setting the price.

### Mission: 
Predict housing price using supervised machine learning models based on Kaggle’s “USA Housing Listings” data that scrapped from Craigslist (the world’s largest collection of privately sold housing options) in Jan. 2020. 

The web app will enable users to input their preferences on housing features and get an estimated price in several seconds. 

Data source: https://www.kaggle.com/austinreese/usa-housing-listings

### Success criteria:
* Machine Learning performance metric:  

  Given the range of the housing price (rent per month) in the data is approximately from $500 to $2,000, the best predictive model should achieve Root Mean Square Error (RMSE) less than $100. From the perspective of homebuyers, a difference of $100 (per month) between the predicted price and the truth is reasonable/acceptable and thus the app would be considered as useful.
  
  To further investigate the model performance for different populations, the RMSE for different types of housing (apartment vs. house vs. condo etc.) or the RMSE for different states in US will be evaluated. 

* Business outcome metric:
  1. The number of visits (by different users) to the web app per week exceeds 700 (approximately 100 users/day).
  2. Those users who have visited the web app to predict housing price will be contacted later asking for their experience. The satisfaction rate should be greater than 70%.

## Planning

### **Initiative 1**: Develop a well-performed machine learning model for predicting housing price.

*	**Epic 1**: *explore data and gain insights from features* 

    * **Story 1**: plot histogram to visualize the distribution of each variable, detect outliers and skewness
    *	**Story 2**: check descriptive statistics of each variable and correlation among them, detect multicollinearity
    *	**Story 3**: draw a heatmap (using latitude and longitude) to visualize where housing listings are located 
    *	**Story 4**: identify variations in price by state and by region to investigate significant difference
    *	**Story 5**: plot pie charts to visualize the makeup of housing types, laundry options, and parking options

*	**Epic 2**: *train a baseline model for use in production*

    *	**Story 1**: scope determining – try different sampling methods to reduce the size of data (originally 384,977 observations), such as stratified sampling based on region
    *	**Story 2**: data cleaning – remove useless columns, correct erroneous/inconsistent data, treat outliers, impute missing values, transform and standardize variables, etc.
    *	**Story 3**: feature engineering – generate new features, reduce levels of categorical variables by grouping similar classes, perform feature selection, conduct one-hot encoding, etc.
    *	**Story 4**: split data into training and test sets (70:30 ratio)
    *	**Story 5**: build and train a linear regression model and get baseline results

*	**Epic 3**: *improve upon the baseline model for better prediction results*

    *	**Story 1**: build and train other machine learning models, such as Ridge regression, Lasso regression, K-nearest Neighbors, Decision Tree, Random Forests, Gradient Boosting Machine
    *	**Story 2**: tune hyperparameters for each candidate model through 10-fold cross validation and select the best set of parameters for each model based on cross validation RMSE
    *	**Story 3**: choose the best model based on prediction accuracy, model interpretability, and computational expenditure, then predict on the test set and see the results (RMSE and 95% confidence interval)
    *	**Story 4**: refit the selected model on the whole cleaned dataset and create table in database to store fitted parameters
    *	**Story 5**: evaluate feature importance and determine features to be put on web app for user inputs
    * **Story 6**: code review, logging, and testing for reproducibility

*	**Epic 4**: *update the best model with newly scraped data (given the housing market changes frequently and the data is scraped every few months)*

    *	**Story 1**: apply the similar data processing pipeline to the new data to make it ready for model
    *	**Story 2**: train the optimal model above on the new training data and report performance metrics on the held-out test set
    *	**Story 3**: make the final model ready for deployment (i.e., repeat “Initiative1.epic3.story4”)

### **Initiative 2**: Deploy an interactive web application that takes housing features from user and output predicted housing price in several seconds.

*	**Epic 1**: *Design User Interface for interaction*
    
    *	**Story 1**: setup the layout and design for the HTML
    *	**Story 2**: add user input functionality
    *	**Story 3**: display results and improve the UI if necessary

*	**Epic 2**: *Deploy the web app (Flask) onto AWS*

*	**Epic 3**: *Use an S3 bucket to store raw source data and create an RDS instance*

*	**Epic 4**: *Testing (both unit tests and configured reproducibility tests)*

*	**Epic 5**: *App improvement – provide more insights to users in addition to the predicted price*

## Backlog
1.	“Initiative1.epic1.story1” (0 point) – PLANNED 
2.	“Initiative1.epic1.story2” (0 point) – PLANNED 
3.	“Initiative1.epic1.story3” (1 point) – PLANNED 
4.	“Initiative1.epic1.story4” (1 point) – PLANNED 
5.	“Initiative1.epic1.story5” (0 point) – PLANNED 
6.	“Initiative1.epic2.story1” (2 points) – PLANNED
7.	“Initiative1.epic2.story2” (4 points) – PLANNED
8.	“Initiative1.epic2.story3” (4 points) – PLANNED
9.	“Initiative1.epic2.story4” (0 point) – PLANNED
10.	 “Initiative1.epic2.story5” (2 points) – PLANNED
11.	 “Initiative1.epic3.story1” (4 points) – PLANNED
12.	 “Initiative2.epic1.story1” (4 points) – PLANNED
13.	 “Initiative1.epic3.story2” (4 points)
14.	“Initiative1.epic3.story3” (2 points)
15.	 “Initiative1.epic3.story4” (2 points)
16.	 “Initiative1.epic3.story5” (1 points)
17.	“Initiative2.epic1.story2” (4 points)
18.	“Initiative1.epic3.story6” (4 points)

## Icebox

*	“Initiative1.epic4.story1”
*	“Initiative1.epic4.story2”
*	“Initiative1.epic4.story3”
*	“Initiative2.epic1.story3”
*	“Initiative2.epic2”
*	“Initiative2.epic3”
*	“Initiative2.epic4”
*	“Initiative2.epic5”

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app
### 1. Initialize the database 

#### Create the database with a single song 
To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create_db --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db` with the initial song *Radar* by Britney spears. 
#### Adding additional songs 
To add an additional song:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.
