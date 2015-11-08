from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.objectid import ObjectId
from utils.mongo_json_encoder import JSONEncoder

# Basic Setup
app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.develop_database
api = Api(app)

class User(Resource):

# Provide an endpoint that allows a client to register a new user by providing username and password
    def post(self):
        new_user = request.json
        # print(new_user)
        user_collection = app.db.users
        result = user_collection.insert_one(new_user)
        user = user_collection.find_one({"_id": ObjectId(result.inserted_id)})
        return user

# Implement REST Resource
class Trip(Resource):

    def post(self):
        new_trip = request.json
        trip_collection = app.db.trips
        result = trip_collection.insert_one(new_trip)
        trip = trip_collection.find_one({"_id": ObjectId(result.inserted_id)})
        return trip

    # Note: implement specific trip via its ID
    def get(self, trip_id):
        trip_collection = app.db.trips
        trip = trip_collection.find_one({"_id": ObjectId(trip_id)})
        if trip is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            return trip



    # Note: Implement all trips via a specific user


    # Note: implement put method
    def put(self, trip_id):
        trip_collection = app.db.trips
        trip = trip_collection.update_one({"_id": ObjectId(trip_id)}, {"$set": request.json})
        trip = trip_collection.find_one({"_id": ObjectId(trip_id)})

        if trip is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            return trip

    # Note: implement delete method
    def delete(self, trip_id):
        trip_collection = app.db.trips
        trip = trip_collection.delete_one({"_id": ObjectId(trip_id)})
        trip = trip_collection.find_one({"_id": ObjectId(trip_id)})
        return {"objectIdentifier": trip_id}
        # if myobject is None:
        #     response = jsonify(data=[])
        #     response.status_code = 404
        #     return response
        # else:
        #     return myobject

# Add REST resource to API
api.add_resource(Trip, '/trip/','/trip/<string:trip_id>')
api.add_resource(User, '/user/')

# provide a custom JSON serializer for flaks_restful
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp

if __name__ == '__main__':
    # Turn this on in debug mode to get detailled information about request related exceptions: http://flask.pocoo.org/docs/0.10/config/
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
