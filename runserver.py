# -*- coding: utf-8 -*-

import feedparser
from app import app, database, csrf
from models import User, Feed
from auth import login_app
from flask import render_template, request, redirect, url_for, session
from functools import wraps
from flask_login import logout_user, LoginManager, current_user


def login_requested(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/login')
def login():
    provider = request.args.get('provider')
    if provider == 'google':
        return login_app('google')
    if provider == 'github':
        return login_app('github')
    if provider == 'facebook':
        return login_app('facebook')
    return render_template('login.html')


@app.route("/logout")
@login_requested
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/index")
@login_requested
def index():
    return render_template('index.html')


@app.route("/new?feed", methods=['GET', 'POST'])
@login_requested
def new_feed():
    if request.method == 'POST':
        feed_url = request.form['feed_url']
        d = feedparser.parse(feed_url)
        '''Parseamos el feed, viendo si esta bien formado'''
        if d.bozo:
            return render_template('newfeed.html',
                                   error_message='Feed malformed')
        if ' ' in feed_url:
            return render_template('newfeed.html',
                                   error_message='Invalid URL')
        feed = Feed.select().where(Feed.url == feed_url)
        i = 0
        new_feed = True
        '''Vemos si el feed ya fue agregado'''
        while i < len(feed):
            if feed[i].user_id == current_user.id:
                new_feed = False
                break
            i = i+1
        '''Verificamos si el feed es nuevo o si el usuario ya lo agrego'''
        if len(feed) == 0 or ((len(feed) != 0) and new_feed):
            '''Comprobamos si la descripcion del feed existe'''
            try:
                Feed.create(url=feed_url,
                            title=d['feed']['title'],
                            description=d['feed']['description'],
                            user=current_user.id)
                return render_template('index.html')
            except (KeyError, AttributeError):
                '''Comprobamos si el feed cumple el protocolo'''
                try:
                    Feed.create(url=feed_url,
                                title=d['feed']['title'],
                                description='',
                                user=current_user.id)
                    return render_template('index.html')
                except (KeyError, AttributeError):
                    return render_template('newfeed.html',
                                           error_message='Url is not a feed')
        return render_template('newfeed.html',
                               error_message='Feed is already present')
    return render_template('newfeed.html')


@app.route("/delete?feed")
@login_requested
def delete_feed():
    feed_id = request.args.get('feed')
    feed = Feed.get(Feed.id == feed_id)
    feed.delete_instance()
    return redirect(url_for('index'))


@app.route('/rss')
@login_requested
def rss():
    feed_id = request.args.get('feed')
    feed = Feed.get(Feed.id == feed_id)
    d = feedparser.parse(feed.url)
    return render_template('rss.html',
                           entries=d.entries,
                           feed=feed)


def main():
    database.create_tables([User, Feed], safe=True)
    app.run()


if __name__ == "__main__":
    main()
