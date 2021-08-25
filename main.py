from flask import Flask, redirect, url_for, render_template, request, session
from flask_discord import DiscordOAuth2Session, Unauthorized
from discord.ext import ipc

import os
import secret

application = Flask(__name__)

ipc_client = ipc.Client( secret_key = secret.IPC_SECRET_KEY )
#os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"


application.config['SECRET_KEY'] = secret.SECRET_KEY
application.config['DISCORD_CLIENT_ID'] = secret.DISCORD_CLIENT_ID
application.config['DISCORD_CLIENT_SECRET'] = secret.DISCORD_CLIENT_SECRET
application.config['DISCORD_REDIRECT_URI'] = secret.DISCORD_REDIRECT_URI

discord = DiscordOAuth2Session(application)



@application.route('/')
def index():
	return render_template('index/index.html', authorized = discord.authorized)


@application.route('/login')
def login():
	return discord.create_session(scope = ['identify', 'guilds'])


@application.route('/callback')
def callback():
	discord.callback()
	return redirect(url_for('dashboard'))


@application.route('/dashboard')
def dashboard():

	user = discord.fetch_user()

	return render_template('dashboard/index.html', authorized = discord.authorized, user = user)


@application.route('/commands')
def commands():

	return render_template('commands/index.html', authorized = discord.authorized)


@application.route('/support')
def support():
	return render_template('support/index.html', authorized = discord.authorized)


@application.route('/logout')
def logout():
	discord.revoke()
	return redirect(url_for('index'))


@application.route('/version')
def version():
	return 'v0.1.3(от 25.08.2021)'



@application.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))


@application.errorhandler(404)
def page_not_found(e):
	return render_template('errors/404.html'), 404



if __name__ == '__main__':
	application.run( debug=False, host='0.0.0.0' )