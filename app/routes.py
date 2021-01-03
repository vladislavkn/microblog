from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime
from .forms import LoginForm, RegistrationForm, EditProfileForm, PostForm

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(body=form.body.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your post is now live!')
    return redirect(url_for('index'))
  page = request.args.get('page', 1, type=int)
  posts = current_user.related_posts().order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
  next_url = url_for('index', page=posts.next_num) if posts.has_next else None
  prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None

  return render_template('pages/index.html', posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)

@app.route('/explore')
def explore():
  page = request.args.get('page', 1, type=int)
  posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
  next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
  prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None

  return render_template('pages/index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)

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
    return redirect(url_for('index'))

  return render_template('pages/register.html', form=form)

@app.route('/user/<name>')
@login_required
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', name=name, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', name=name, page=posts.prev_num) if posts.has_prev else None

    return render_template('pages/user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_name=current_user.name)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', name=current_user.name))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.about_me.data = current_user.about_me
    return render_template('pages/edit_profile.html', form=form)

@app.route('/follow/<name>')
@login_required
def follow(name):
  user = User.query.filter_by(name=name).first()
  if user is None:
    flash(f'User {name} not found.')
    return redirect(url_for('index'))
  if user == current_user:
    flash('You cannot follow yourself!')
    return redirect(url_for('user', name=name))
  current_user.follow(user)
  db.session.commit()
  flash(f'You are following {name}!')
  return redirect(url_for('user', name=name))

@app.route('/unfollow/<name>')
@login_required
def unfollow(name):
  user = User.query.filter_by(name=name).first()
  if user is None:
    flash(f'User {name} not found.')
    return redirect(url_for('index'))
  if user == current_user:
    flash('You cannot unfollow yourself!')
    return redirect(url_for('user', name=name))
  current_user.unfollow(user)
  db.session.commit()
  flash(f'You are not following {name}.')
  return redirect(url_for('user', name=name))