
from flask import render_template, url_for, flash, redirect, request, session, Blueprint
from flask import current_app as app
from flask_login import login_user, current_user, logout_user, login_required

from app import db, bcrypt
from app.models import User
from app.views.users.forms import ( RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm )
from app.views.users.utils import save_picture, send_reset_email

from oauthlib.oauth2 import WebApplicationClient


import requests
import json
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

users = Blueprint('users', __name__)

client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

# Email Authentication

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('auth/register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash('Successfuly logged out.' , 'primary')
    return redirect(url_for('main.home'))


# Google Authentication

def get_google_provider_cfg():
    return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()


@users.route('/google/login')
def google_auth():

    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
    )

    return redirect(request_uri)


@users.route('/google/login/callback')
def google_callback():

    code = request.args.get('code')

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET']),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get('email_verified'):
        users_email = userinfo_response.json()['email']
        picture = userinfo_response.json()['picture']
        users_name = userinfo_response.json()['given_name']
    else:
        flash('User email not available or not verified by Google.')
        print('User email not available or not verified by Google.')

    user = User.query.filter_by(email=users_email).first()

    if not user:
        user = User(username=users_email, email=users_email, image_file=picture)
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=True)

    return redirect(url_for('main.dashboard'))


# User Account

@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():

    return render_template('auth/profile.html', username=current_user.username, avatar=current_user.image_file)


# Reset Passwords

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('auth/reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)
