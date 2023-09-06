from flask import Flask, render_template, redirect, url_for, flash, abort, request, jsonify
from pymongo import MongoClient
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://localhost:27017/')

db = client['test-database']
collection = db['test-collection']


class Users(Resource):
    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Name cannot be blank!")
        parser.add_argument('password', required=True, help="Name cannot be blank!")
        parser.add_argument('email', required=True, help="Name cannot be blank!")

        args = parser.parse_args()
        print("USERNAME::::::s"+args['username'])
        collection.insert_one({'username': args['username'], 'email': args['email'], 'password': args['password']})
        return jsonify(args)
        
    


@app.route('/add_data')
def add_data():
    collection.insert_one({'name': 'John'})
    return 'Added Data!'

@app.route('/add_data1')
def add_data1():
    collection.insert_one({'name': 'Orvil'})
    return 'Added Data!'

@app.route('/')
def hello_world():
    return 'Hello World!'


api.add_resource(Users, '/users')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)