from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, ReviewForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from textblob import TextBlob


@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/home", methods=['GET', 'POST'])
def home():
    ans=''
    test=[]
    form = ReviewForm()
    if form.validate_on_submit():
        ans=form.reviewdata.data
        testimonial = TextBlob(ans)
        analysis=str(testimonial.sentiment.polarity)
        test.append(current_user.username)
        test.append(str(testimonial))
        test.append(analysis)
        post = Post(title=analysis, content=str(testimonial), author=current_user)
        db.session.add(post)
        db.session.commit()
    return render_template('home.html',title='home',form=form,results=test)


@app.route("/about")
def about():
    test=[]
    test.append(analize())
    return render_template('about.html', title='About',results=test)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

def analize():
    analized_data=[]
    alldata=Post.query.all()
    for data in alldata:
        temp_data=data.title
        analized_data.append(float(temp_data))
    
    avg_data=sum=0
    for data in analized_data:
        sum= sum+data
    avg_data=float(sum/(len(analized_data)))
    return avg_data