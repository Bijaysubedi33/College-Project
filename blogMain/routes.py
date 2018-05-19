from flask import render_template, url_for,flash,redirect
from blogMain.form import Registration_Form,Login_Form
from blogMain import app,db,bcrypt,login
from blogMain.models import User,Post
from flask_login import login_user,current_user,logout_user

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },

    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]
@app.route("/",methods = ['GET','POST'])
@app.route("/home",methods = ['GET','POST'])
def home():
    return render_template('home.html', posts=posts)

@app.route("/about",methods = ['GET','POST'])
def about():
    return render_template('about.html', title='About')

@app.route("/category")
def category():
    return render_template('category.html')

@app.route("/register",methods = ['GET','POST'])
def register():
    form =Registration_Form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account is created {}'.format(form.username.data), 'success')
        return redirect(url_for('login'))

    return render_template('registration.html',title = 'Register' ,form = form)


@app.route("/login",methods = ['GET','POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('user'))
        else:
            flash('Please give a valid email and password', 'danger')

    return render_template('login.html', title='Login',form=form)

@app.route("/dashboard",methods = ['GET','POST'])
def user():
    form = Registration_Form()
    return render_template('user.html',user = form.username.data)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
