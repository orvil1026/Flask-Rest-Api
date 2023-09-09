from flask import Flask, jsonify
from pymongo import MongoClient
from flask_restful import Resource, Api, reqparse
from bson import json_util, ObjectId
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")

db = client['test-database']
collection = db['test-collection']


def parse_json(data):
    return json.loads(json_util.dumps(data))


#Get all users and add new user
class Users(Resource):

    # get all users
    def get(self):
        result = []
        for user in collection.find():
            result.append(user)
            
        return parse_json(result)   
     
    # add a user
    def post(self):
        #get the data from the request
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Name cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        parser.add_argument('email', required=True, help="Email cannot be blank!")

        args = parser.parse_args()

        #check if username and email already exists
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


#Get a user by id, update a user by id, delete a user by id
class UserIdSpecific(Resource):

    # get a user by id
    def get(self, id):
        
        if len(id) == 24:
            result = []
            cursor = collection.find({"_id": ObjectId(id)})
            for doc in cursor:
                result.append(doc)

            if result == []:
                return jsonify({'status':'error','message': 'No User present with that ID!'})
            return parse_json(result)

        else:
            return jsonify({'status':'error','message': 'Invalid ID!'})
          
    # delete a user by id
    def delete(self, id):
        try:
            result = []
            cursor = collection.find_one_and_delete({"_id": ObjectId(id)})

            if cursor == None:
                raise Exception('No User present with that ID!')

        except Exception as e: 
            return jsonify({'status':'error','message': 'No User present with that ID!'})
    
        return jsonify({'status':'success','message': 'User Deleted Successfully!'})

    # update a user by id
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('email')

        args = parser.parse_args()

        try:

            #getting the old values
            result = []
            cursor = collection.find({"_id": ObjectId(id)})
            for doc in cursor:
                result.append(doc)

            #getting the new values
            oldUsername = result[0]['username']
            oldEmail = result[0]['email']
            oldPassword = result[0]['password']

            newUsername = args['username']
            newEmail = args['email']
            newPassword = args['password']

            #check if new username, email and password is None and if it is then assign the old values
            if newUsername == None:
                newUsername = oldUsername
            if newEmail == None:
                newEmail = oldEmail
            if newPassword == None:
                newPassword = oldPassword


            cursor = collection.find_one_and_update({"_id": ObjectId(id)}, { "$set": { "username": newUsername, "password": newPassword, "email": newEmail } },)
            if cursor == None:
                raise Exception('No User present with that ID!')

        except Exception as e: 
            print(e)
            return jsonify({'status':'error','message': 'No User present with that ID!'})
    
        return jsonify({'status':'success','message': 'User Updated Successfully!'})

#add the resources
api.add_resource(Users, '/users')
api.add_resource(UserIdSpecific, '/users/<id>')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)