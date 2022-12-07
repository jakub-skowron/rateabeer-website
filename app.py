from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beer_website_DB.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0vVH3jTxz5PWaiyfkaLJ@containers-us-west-110.railway.app:6377/railway'
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


