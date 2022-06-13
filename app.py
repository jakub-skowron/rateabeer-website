from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beer_website_DB.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pxmfttvrjxgvyx:1105d29793a2ce9d462ea5666bc8bf10d26cbd622c3e2661e7254cb6358b4452@ec2-34-231-221-151.compute-1.amazonaws.com:5432/dc1q57uqeehoee'
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
    app.run(debug=True)


