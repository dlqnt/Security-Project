from flask import render_template, flash, redirect, url_for, request, session, abort
from app import app, query_db, valid_login, add_user, get_user_by_username, insert_comment, insert_image, get_post, insert_friend, update_userinfo, get_detailsUser
from app.forms import IndexForm, PostForm, FriendsForm, ProfileForm, CommentsForm
from datetime import datetime
from werkzeug.security import generate_password_hash
import os
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
# this file contains all the different routes, and the logic for communicating with the database

# home page/login/registration
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = IndexForm()

    if form.login.validate_on_submit() and form.login.submit.data:
        login = valid_login(form.login.username.data, form.login.password.data)

        if not login:
            abort(404)
        if login == None:
            flash('Sorry, this user does not exist!')
        elif login:
            user = get_user_by_username(form.login.username.data)
            session["id"] = user["id"]
            return redirect(url_for('stream', username=form.login.username.data))
        else:
            flash('Sorry, wrong password!')

    elif form.register.validate_on_submit() and form.register.submit.data:
        add_user(form.register.username.data, form.register.first_name.data, form.register.last_name.data, generate_password_hash(form.register.password.data))
        return redirect(url_for('index'))
    return render_template('index.html', title='Welcome', form=form)

@app.route('/stream/<username>', methods=['GET', 'POST'])
def stream(username):
    userid = session.get("id", None)
    user = get_user_by_username(username)
    if userid == None or userid != user["id"]:
        abort(404)
    form = PostForm()
    user = get_user_by_username(username)
    if form.validate_on_submit():
        if form.image.data:
            path = os.path.join(app.config['UPLOAD_PATH'], form.image.data.filename)
            form.image.data.save(path)


        insert_image(user['id'], form.content.data, form.image.data.filename, datetime.now())
        return redirect(url_for('stream', username=username))

    posts = query_db('SELECT p.*, u.*, (SELECT COUNT(*) FROM Comments WHERE p_id=p.id) AS cc FROM Posts AS p JOIN Users AS u ON u.id=p.u_id WHERE p.u_id IN (SELECT u_id FROM Friends WHERE f_id={0}) OR p.u_id IN (SELECT f_id FROM Friends WHERE u_id={0}) OR p.u_id={0} ORDER BY p.creation_time DESC;'.format(user['id']))
    return render_template('stream.html', title='Stream', username=username, form=form, posts=posts)

@app.route("/logout")
def logout():
    session.pop("id")
    form = IndexForm()
    return redirect(url_for('index'))
    

# comment page for a given post and user.
@app.route('/comments/<username>/<int:p_id>', methods=['GET', 'POST'])
def comments(username, p_id):
    userid = session.get("id", None)
    user = get_user_by_username(username)
    if userid == None or userid != user["id"]:
        abort(404)
    form = CommentsForm()
    if form.validate_on_submit():
        user = get_user_by_username(username)
        insert_comment(user["p_id"], user["u_id"], form.comment.data, datetime.now())
    post = get_post(p_id)
    all_comments = query_db('SELECT DISTINCT * FROM Comments AS c JOIN Users AS u ON c.u_id=u.id WHERE c.p_id={} ORDER BY c.creation_time DESC;'.format(p_id))
    return render_template('comments.html', title='Comments', username=username, form=form, post=post, comments=all_comments)

# page for seeing and adding friends
@app.route('/friends/<username>', methods=['GET', 'POST'])
def friends(username):
    userid = session.get("id", None)
    user = get_user_by_username(username)
    if userid == None or userid != user["id"]:
        abort(404)
    form = FriendsForm()
    user = get_user_by_username(username)
    if form.validate_on_submit():
        friend = get_user_by_username(form.username.data)
        if friend is None:
            flash('User does not exist')
        else:
            insert_friend(user['id'], friend['id'])
    
    all_friends = query_db('SELECT * FROM Friends AS f JOIN Users as u ON f.f_id=u.id WHERE f.u_id={} AND f.f_id!={} ;'.format(user['id'], user['id']))
    return render_template('friends.html', title='Friends', username=username, friends=all_friends, form=form)

# see and edit detailed profile information of a user
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    userid = session.get("id", None)
    user = get_user_by_username(username)
    if userid == None or  userid != user["id"]:
        abort(404)
    
    form = ProfileForm()
    if form.validate_on_submit():
        update_userinfo(form.education.data, form.employment.data, form.music.data, form.movie.data, form.nationality.data, form.birthday.data, username)
        return redirect(url_for('profile', username=username))
    
    user =  get_detailsUser(username)
    return render_template('profile.html', title='profile', username=username, user=user, form=form)

@app.route('/friend/<username>', methods=['GET'])
def friend(username):
    userid = session.get("id", None)
    user = get_user_by_username(username)
    if userid == None or user["id"] == None:
        abort(404)
    form = ProfileForm()
    
    user =  get_detailsUser(username)
    return render_template('profile.html', title='profile', username=username, user=user, form=form)
