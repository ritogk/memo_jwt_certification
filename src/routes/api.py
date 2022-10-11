from urllib.parse import unquote
import base64
from controllers.oauth_controller import OAuthController
from flask import jsonify, render_template, make_response, request, Blueprint
from controllers.authentication_controller.authentication_controller import AuthenticationController
from controllers.user_controller import UserController
user_controller = UserController()
authentication_controller = AuthenticationController()
oauth_controller = OAuthController()

api = Blueprint("api", __name__)


@api.route('/users', methods=['POST'])
# ユーザー登録(password)
def users():
    return user_controller.create()


@api.route('/users/login', methods=['POST'])
# ログイン(password)
def users_login():
    return user_controller.login()


@api.route('/users/oauth/twitter', methods=['POST'])
# ユーザー登録(twitter)
def users_oauth_twitter():
    return oauth_controller.create_twitter_user()


@api.route('/users/oauth/twitter/login', methods=['POST'])
# ユーザーログイン(twitter)
def users_oauth_twitter_login():
    return oauth_controller.users_oauth_twitter_login()


@api.route('/users/oauth/google', methods=['POST'])
# ユーザー新規登録(google)
def users_oauth_google():
    return oauth_controller.create_google_user()


@api.route('/users/oauth/google/login', methods=['POST'])
# ユーザーログイン(google)
def users_oauth_google_login():
    return oauth_controller.users_oauth_google_login()


@api.route('/oauth/google/url', methods=['GET'])
# ユーザー登録(google)
def oauth_google_url():
    return oauth_controller.oauth_google_url()


@api.route('/oauth/twitter/url', methods=['GET'])
# twitterの認証画面のurlを取得
def oauth_twitter_url():
    return oauth_controller.oauth_twitter_url()
