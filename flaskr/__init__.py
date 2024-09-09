from flask import Flask, jsonify
from flask_restful import Api, Resource
from flaskr.api_client import fetch_disaster_data
from asgiref.sync import async_to_sync
# from flaskr.config import settings
import psycopg2

# def check_database():
#     try:
#         conn=psycopg2.connect(settings.DATABASE_URL)
#         conn.close()
#         return True
#     except Exception as e:
#         print(f"Error connecting : ${str(e)}")
#         return False


class HealthCheck(Resource):
    def get(self):
        isDbConnected=True
        return {"status":"healthy", "message":"Service is running", "database": "connected" if isDbConnected else "disconnected"},200

class DistrictData(Resource):
    def get(self):
        try:
            data=async_to_sync(fetch_disaster_data)()
            return {"data":data},200

        except Exception as e:
            return {"error":str(e)}, 500

def create_app():
    app = Flask(__name__)
    api = Api(app)
    
    # Add routes here
    api.add_resource(HealthCheck, '/')
    api.add_resource(DistrictData, '/api/v1/districts')
    
    return app
