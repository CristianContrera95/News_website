# -*- coding: utf-8 -*-

from app import app, database, lm
from models import User, AnonymousUser
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import session
from flask_login import LoginManager
from flask_login import logout_user, current_user, login_required
from flask_login import login_user
from flask_oauthlib.client import OAuth, OAuthException


oauth = OAuth(app)
oauth.init_app(app)


github = oauth.remote_app(
    'github',
    consumer_key='947470d4152f1c30f879',
    consumer_secret='dddbb4da0d8a2c26b7790b0aca13a937b9812b66',
    request_token_params={'scope': 'user:emails'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

google = oauth.remote_app(
    'google',
    consumer_key='268045696293-upqhuvt2e0aug8dj891l366776rf3ieh' +
    '.apps.googleusercontent.com',
    consumer_secret='gVxHJwPrSE815gVWJM-wzWWT',
    request_token_params={'scope': 'email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


facebook = oauth.remote_app(
    'facebook',
    consumer_key='1001253953328127',
    consumer_secret='7f774f1565cdc20bc798a4b107d7107c',
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)


@lm.user_loader
def load_user(user):
    try:
        return User.get(User.id == user)
    except User.DoesNotExist:
        session.clear()
        return AnonymousUser()


def login_app(app):
    if app == 'github':
        return github.authorize(
            callback=url_for('authorized_pag',
                             login='login',
                             autho='authorized?github',
                             _external=True))
    elif app == 'google':
        return google.authorize(
            callback=url_for('authorized_pag',
                             login='login',
                             autho='authorized?google',
                             _external=True))
    elif app == 'facebook':
        return facebook.authorize(
            callback=url_for('authorized_pag',
                             login='login',
                             autho='authorized?facebook',
                             next=(request.args.get('next') or
                                   request.referrer or None),
                             _external=True))


@app.route('/<login>/<autho>')
def authorized_pag(login=None, autho=None):
    preid = ''
    if autho == 'authorized?google':
        preid = 'GO'
        resp = google.authorized_response()
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        session['google_token'] = (resp['access_token'], '')
        me = google.get('userinfo')
    elif autho == 'authorized?github':
        preid = 'GI'
        resp = github.authorized_response()
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error'],
                request.args['error_description']
            )
        session['github_token'] = (resp['access_token'], '')
        me = github.get('user')
    elif autho == 'authorized?facebook':
        preid = 'FA'
        resp = facebook.authorized_response()
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        if isinstance(resp, OAuthException):
            return 'Access denied: %s' % resp.message
        session['oauth_token'] = (resp['access_token'], '')
        me = facebook.get('me?fields=id,email,name')
        if me.data.get('email') is None:
            me.data['email'] = None
    '''Selecionamos los usuarios con el 'id' dado, formando una lista'''
    user = User.select().where(User.social_id == (preid + str(me.data['id'])))
    '''Si la lista es vacia, el usuario no esta registrado'''
    if len(user) == 0:
        if me.data['name'] is None:
            me.data['name'] = str(me.data['login'])
        user = User.create(nickname=me.data['name'],
                           social_id=preid + str(me.data['id']),
                           email=me.data['email'])
    else:
        user = user[0]
    login_user(user, True)
    return redirect(url_for("index"))


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
