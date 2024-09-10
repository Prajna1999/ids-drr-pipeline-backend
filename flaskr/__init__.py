# flaskr/__init__.py

from flask import Flask, jsonify, request, g
from flask_restful import Api, Resource
from functools import wraps
from flaskr.api_client import fetch_disaster_data
from asgiref.sync import async_to_sync
import requests

# Decorator for verifying the JWT


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # JWT is passed in the request header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        # Return 401 if token is not passed
        if not token:
            return {'message': 'Token is missing!'}, 401

        # Store the token in Flask's g object for access in the route
        g.token = token
        return f(*args, **kwargs)
    return decorated


class HealthCheck(Resource):
    def get(self):
        isDbConnected = True
        return {"status": "healthy", "message": "Service is running", "database": "connected" if isDbConnected else "disconnected"}, 200


class DistrictData(Resource):
    @token_required
    def get(self):
        try:
            data = async_to_sync(fetch_disaster_data)()
            return {"data": data}, 200
        except Exception as e:
            return {"error": str(e)}, 500


class Login(Resource):
    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        # Call the external authentication API
        response = requests.post('https://drims.veldev.com/api/auth/local',
                                 json={"identifier": username, "password": password})

        if response.status_code == 200:
            return response.json(), 200
        else:
            return {"message": "Invalid username or password"}, 401


def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Add routes here
    api.add_resource(HealthCheck, '/')
    api.add_resource(DistrictData, '/api/v1/districts')
    api.add_resource(Login, '/login')

    return app
