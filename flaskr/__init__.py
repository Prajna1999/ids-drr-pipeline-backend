# flaskr/__init__.py

from flask import Flask, jsonify, request, g
from flask_restful import Api, Resource
from functools import wraps
from flaskr.api_client import fetch_disaster_data, fetch_consolidated_flood_data
from asgiref.sync import async_to_sync
from datetime import datetime, timedelta
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


class ConsolidatedFloodData(Resource):
    @token_required
    def get(self):
        try:
            from_date = request.args.get('fromDate')
            to_date = request.args.get('toDate')

            if not from_date or not to_date:
                return {
                    "error": "Both fromDate and toDAte are required"
                }, 400
            try:
                datetime.strptime(from_date, "%Y-%m-%d")
                datetime.strptime(to_date, "%Y-%m-%d")

            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400

            if from_date > to_date:
                return {"error": "fromDate cannnot be after toDate"}, 400

            # call the api
            data = async_to_sync(fetch_consolidated_flood_data)(
                from_date, to_date)

            return {"data": data}, 200
        except Exception as e:
            return {"error": str(e)}, 500


class Login(Resource):
    def post(self):
        identifier = request.json.get('identifier', None)
        password = request.json.get('password', None)

        # Call the external authentication API
        response = requests.post('https://drims.veldev.com/api/auth/local',
                                 json={"identifier": identifier, "password": password})

        if response.status_code == 200:
            return response.json(), 200
        else:
            return {"message": "Invalid username or password"}, 401


def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Add routes here
    api.add_resource(HealthCheck, '/')
    api.add_resource(ConsolidatedFloodData, '/api/v1/flood/consolidated')
    api.add_resource(Login, '/api/v1/login')

    return app
