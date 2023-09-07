from flask import Flask, render_template, redirect, url_for, flash, abort, request, jsonify
from pymongo import MongoClient
from flask_restful import Resource, Api, reqparse
from bson import json_util
import json
import pprint

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://localhost:27017/')

db = client['test-database']
collection = db['test-collection']


def parse_json(data):
    return json.loads(json_util.dumps(data))

class Users(Resource):

    def get(self):
        result = []
        for user in collection.find():
            result.append(user)
            
        return parse_json(result)    

    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Name cannot be blank!")
        parser.add_argument('password', required=True, help="Name cannot be blank!")
        parser.add_argument('email', required=True, help="Name cannot be blank!")

        args = parser.parse_args()

        username_count = collection.count_documents({"username": args['username']})
        email_count = collection.count_documents({"email": args['email']})


        if username_count != 0 and email_count != 0:
            return jsonify({'status':'error','message': 'Username and Email already exists!'})
        elif username_count != 0:
            return jsonify({'status':'error','message': 'Username already exists!'})
        elif email_count != 0:
            return jsonify({'status':'error','message': 'Email already exists!'})
        
        collection.insert_one({'username': args['username'], 'email': args['email'], 'password': args['password']})
        return jsonify({'status':'success','message': 'User Added Successfully!'})
        

# @app.route('/add_data')
# def add_data():
#     collection.insert_one({'name': 'John'})
#     return 'Added Data!'

# @app.route('/add_data1')
# def add_data1():
#     collection.insert_one({'name': 'Orvil'})
#     return 'Added Data!'

# @app.route('/')
# def hello_world():
#     return 'Hello World!'


api.add_resource(Users, '/users')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)