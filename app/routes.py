from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from .forms import LoginForm, RegistrationForm

@app.route('/')
@login_required
def index():
  return render_template('pages/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(name=form.name.data).first()
    if user is None or not user.check_password(form.password.data):
        flash('Invalid username or password')
    else:
      login_user(user, remember=form.remember_me.data)
      next_page = request.args.get('next')
      if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
      return redirect(next_page)

  return render_template('pages/login.html', form=form)

@app.route('/logout')
def logout():
  logout_user()

  return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
      return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(name=form.name.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=form.remember_me.data)
    flash('Congratulations, you are now a registered user!')
    return redirect(url_for('login'))

  return render_template('pages/register.html', form=form)