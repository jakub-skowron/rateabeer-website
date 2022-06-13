from app import app, db
from flask import render_template, redirect, url_for, request, flash
from models import Post, User
from forms import AddNewBeerForm, RegistrationForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

#main site
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=6)
    return render_template("index.html", posts=posts)

#informations about the author
@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

#adding new beer with form
@app.route("/add_new", methods=["GET", "POST"])
@login_required
def add_new():
    form = AddNewBeerForm(csrf_enabled=False)

    if form.validate_on_submit():
        author = current_user.id
        new_beer_post = Post(beer_name=form.beer_name.data, brewery_name=form.brewery_name.data, beer_style=form.beer_style.data, beer_comment=form.beer_comment.data, beer_rate=form.beer_rate.data, user_id = author, timestamp=datetime.utcnow())
        db.session.add(new_beer_post)
        db.session.commit()
        flash("You added your post successufully!")
        return redirect("user/{}".format(current_user))

    return render_template("add_new.html", form=form)

#register site
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(csrf_enabled=False)

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

#user login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password. Try again!")
            return redirect(url_for('login'))

        login_user(user, form.remember_me.data)
        next_page = request.args.get("next")

        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        flash("Hello again {}! You logged in successfully!".format(user.username))
        return redirect(next_page)

    return render_template('login.html', form = form)

#users beer-post list
@app.route('/user/<username>', methods = ['GET', 'POST'])
@login_required
def user(username):
    user = current_user
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username = user.username).first()
    posts = Post.query.filter_by(user_id = user.id).order_by(Post.timestamp.desc()).paginate(page=page, per_page=6)

    if posts is None:
        posts = []

    return render_template('user.html', user = user, posts = posts)

#record updating
@app.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update(id):
    form = AddNewBeerForm(csrf_enabled=False)
    feature_to_update = Post.query.get_or_404(id)

    if request.method == 'POST' and form.validate_on_submit():
        feature_to_update.beer_name = request.form['beer_name']
        feature_to_update.brewery_name = request.form['brewery_name']
        feature_to_update.beer_style = request.form['beer_style']
        feature_to_update.beer_comment = request.form['beer_comment']
        feature_to_update.beer_rate = request.form['beer_rate']
        feature_to_update.timestamp = datetime.utcnow()
        feature_to_update.edition = 'Edited'

        try:
            db.session.commit()
            flash("Post updated successfully!")
            return redirect(url_for('user', username=current_user.username))

        except:
            flash("Ops! Something went wrong. Try again!")
            return render_template("update.html", form = form, feature_to_update = feature_to_update)
            
    else:
        return render_template("update.html", form = form, feature_to_update = feature_to_update)       



#deleting user's beer-post
@app.route("/delete/<int:id>")
def delete(id):
    post_to_delete = Post.query.get_or_404(id)
    try:
        
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post deleted successfully")
        return redirect(url_for('user', username=current_user.username))

    except:
        flash("Something went wrong... Try again...")
        return redirect(url_for('user', username=current_user.username))
    


#user logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You logged out successfully!')
    return redirect(url_for("index"))