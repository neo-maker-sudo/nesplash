import os
from flask import Blueprint, url_for, redirect, abort, session
from nesplash.extensions import oauth, db
from nesplash.models import User, Method
from nesplash.user.util import send_register_mail

oauth_bp = Blueprint("auth", __name__)

github = oauth.remote_app(
    name='github',
    consumer_key=os.getenv("GITHUB_CLIENT_ID"),
    consumer_secret=os.getenv("GITHUB_CLIENT_SECRET_KEY"),
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

google = oauth.remote_app(
    name='google',
    consumer_key=os.getenv('GOOGLE_CLIENT_ID'),
    consumer_secret=os.getenv('GOOGLE_CLIENT_SECRET_KEY'),
    request_token_params={'scope': ['email', 'profile']},
    base_url='https://www.googleapis.com/oauth2/v3/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


providers = {
    'github': github,
    'google': google
}

provider_endpoints = {
    'github': 'user',
    'google': 'userinfo'
}

def get_social_profile(provider, access_token):
    profile_endpoint = provider_endpoints[provider.name]
    response = provider.get(profile_endpoint, token=access_token)
    if provider.name == 'google':
        email = response.data.get('email')
        username = response.data.get('name')
        if username is None:
            splitList = email.split("@")
            username = splitList[0]
        website = response.data.get('link')
        profile_image = response.data.get("picture")
        bio = ''
    else:
        username = response.data.get('login')
        website = response.data.get('html_url')
        email = response.data.get('email')
        if email is None:
            response_again = provider.get('user/emails', token=access_token)
            email = response_again.data[0]["email"]
        profile_image = response.data.get('avatar_url')
        bio = response.data.get('bio')

    return username, email, website, bio, profile_image


@oauth_bp.route("/login/<provider_name>")
def oauth_login(provider_name):
    if provider_name not in providers.keys():
        abort(404)

    if session.get("email"):
        return redirect(url_for("main.index"))

    callback = url_for('auth.oauth_callback', provider_name=provider_name , _external=True, _scheme="https")
    return providers[provider_name].authorize(callback=callback)


@oauth_bp.route("/callback/<provider_name>")
def oauth_callback(provider_name):
    if provider_name not in providers.keys():
        abort(404)
    
    provider = providers[provider_name]
    response = provider.authorized_response()

    if response is not None:
        access_token = response.get('access_token')
    else:
        access_token = None

    if access_token is None:
        return redirect(url_for('user.signin'))

    username, email, website, bio, profile_image = get_social_profile(provider, access_token)

    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(
            username=username,
            email=email,
            bio=bio,
            profile_image=profile_image,
            link=website,
            methods=Method.query.filter_by(name=f"{provider_name}").first(),
        )
        db.session.add(user)
        db.session.commit()
        session["email"] = email
        send_register_mail(user)
        return redirect(url_for('user.person_data'))
    else:
        if user.useAuthy is True:
            session["email"] = user.email
            return redirect(url_for('authy.twofa_token'))
        else:
            session["email"] = user.email
            return redirect(url_for('main.index'))
