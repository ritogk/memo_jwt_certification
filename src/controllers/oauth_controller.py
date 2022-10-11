from flask import current_app
import random
from service.GoogleAuthService import GoogleAuthService
from service.TwitterAuthService import TwitterAuthService
from os import access
from flask import request, redirect, jsonify, url_for, make_response, current_app
from controllers.authentication_controller.forms import UserLoginForm
from db.db import db
from db.models.all import User
import jwt
from service.UserService import UserService
user_service = UserService()

twitter_auth_service = TwitterAuthService()
google_auth_service = GoogleAuthService()


class OAuthController:
    def __init__(self) -> None:
        pass
    # twitterの認証画面URLを取得します。

    def oauth_twitter_url(self):
        # twitterの認証画面のurlを取得
        url = twitter_auth_service.get_authorization_url()
        response = make_response({
            'url': url
        })
        response.headers.set('Content-Type', 'application/json')
        response.headers.add('X-Content-Type-Options', 'nosniff')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # twitter側で認可されたユーザーを登録します。
    def create_twitter_user(self):
        code = request.json["code"]
        # codeからアクセストークンを取得
        access_token, refresh_token = twitter_auth_service.fetch_token(code)
        print(access_token)
        print(refresh_token)
        # twitterからユーザー情報取得
        twitter_user = twitter_auth_service.get_user_info(access_token)

        content = {}
        # ユーザー登録
        user = user_service.create_oauth_user(
            'twitter', twitter_user['data']['name'], twitter_user['data']['id'] + '@' + str(random.random()), twitter_user['data']['id'])
        content["id"] = user.id
        content["name"] = user.name

        # jwt生成
        key = current_app.config['JWT_SECRET']
        token = jwt.encode(content, key, algorithm="HS256").decode('utf-8')
        server_domain = 'server.test.com'

        response = make_response({
            'id': content["id"]
        })
        response.headers.set('Content-Type', 'application/json')
        response.headers.add('X-Content-Type-Options', 'nosniff')
        response.headers.add('Access-Control-Allow-Credentials', 'true')

        response.set_cookie("token", value=token,
                            httponly=True, samesite=None,
                            domain=server_domain, path='/')
        return response

    # twitterのoauthを使ってログインを行います。
    def users_oauth_twitter_login(self):
        code = request.json["code"]
        # codeからアクセストークンを取得
        access_token, refresh_token = twitter_auth_service.fetch_token(code)
        print(access_token)
        print(refresh_token)
        # twitterからユーザー情報取得
        twitter_user = twitter_auth_service.get_user_info(access_token)

        content = {}
        oauth_user = user_service.get_oauth_user(
            'twitter', twitter_user['data']['id'])
        # ログイン
        content["id"] = oauth_user.id
        content["name"] = oauth_user.name

        # jwt生成
        key = current_app.config['JWT_SECRET']
        token = jwt.encode(content, key, algorithm="HS256").decode('utf-8')
        server_domain = 'server.test.com'

        response = make_response({
            'id': content["id"]
        })
        response.headers.set('Content-Type', 'application/json')
        response.headers.add('X-Content-Type-Options', 'nosniff')
        response.headers.add('Access-Control-Allow-Credentials', 'true')

        response.set_cookie("token", value=token,
                            httponly=True, samesite=None,
                            domain=server_domain, path='/')
        return response

    # googleの認証画面URLを取得します。
    def oauth_google_url(self):
        url = google_auth_service.get_authorization_url()
        response = make_response({
            'url': url
        })
        response.headers.set('Content-Type', 'application/json')
        response.headers.add('X-Content-Type-Options', 'nosniff')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # googleに認可されたユーザーを登録します。
    def create_google_user(self):
        code = request.json["code"]
        # codeからアクセストークンを取得
        access_token, refresh_token = google_auth_service.fetch_token(code)
        print(access_token)
        print(refresh_token)
        # googleからユーザー情報取得
        google_user = google_auth_service.get_user_info(access_token)
        print(google_user)

        content = {}
        content["id"] = google_user['id']
        # ユーザー登録
        user = user_service.create_oauth_user(
            'google', google_user['name'], google_user['email'], google_user['id'])

        # jwt生成
        key = current_app.config['JWT_SECRET']
        print(key)
        # content = {}
        token = jwt.encode(content, key, algorithm="HS256").decode('utf-8')
        server_domain = 'server.test.com'

        response = make_response({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })
        response.headers.set('Content-Type', 'application/json')
        response.headers.add('X-Content-Type-Options', 'nosniff')
        response.headers.add('Access-Control-Allow-Credentials', 'true')

        response.set_cookie("token", value=token,
                            httponly=True, samesite=None,
                            domain=server_domain, path='/')
        return response

    # googleのoauthを使ってログインを行います。
    def users_oauth_google_login(self):
        code = request.json["code"]
        # codeからアクセストークンを取得
        access_token, refresh_token = google_auth_service.fetch_token(code)
        print(access_token)
        print(refresh_token)
        # googleからユーザー情報取得
        google_user = google_auth_service.get_user_info(access_token)
        print(google_user)

        content = {}
        oauth_user = user_service.get_oauth_user('google', google_user['id'])
        # ログイン
        content["id"] = oauth_user.id

        # jwt生成
        key = current_app.config['JWT_SECRET']
        print(key)
        token = jwt.encode(content, key, algorithm="HS256").decode('utf-8')
        server_domain = 'server.test.com'

        response = make_response({
            'id': content["id"]
        })
        response.headers.set('Content-Type', 'application/json')
        response.headers.add('X-Content-Type-Options', 'nosniff')
        response.headers.add('Access-Control-Allow-Credentials', 'true')

        response.set_cookie("token", value=token,
                            httponly=True, samesite=None,
                            domain=server_domain, path='/')
        return response
