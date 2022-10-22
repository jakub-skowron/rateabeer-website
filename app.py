from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beer_website_DB.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rtfzteqqckdbzy:d5eb65b8dde9d9d51c3147673c9a19ef3b73133e147b0a063efadbf917baa066@ec2-54-157-16-196.compute-1.amazonaws.com:5432/d3vlahnej3qd5d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)

# ------- Managing logged in state -------
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login' # The name of the view to redirect to when the user needs to log in. 

import routes
#from models import Post
db.create_all()

if __name__ == '__main__':
    app.run()


