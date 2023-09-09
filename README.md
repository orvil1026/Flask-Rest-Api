# Flask-Rest-Api (Flask and MongoDB)

### Routes
* **GET /users** - Returns a list of all users.
* **GET /users/<id>** - Returns the user with the specified ID.
* **POST /users** - Creates a new user with the specified data. (Query Parameters: username, email, password)
* **PUT /users/<id>** - Updates the user with the specified ID with the new data.  (Query Parameters: username, email, password)
* **DELETE /users/<id>** - Deletes the user with the specified ID.

### The User resource have the following fields:
* id (a unique identifier for the user)
* name 
* email 
* password

### Run the Below Command to Start the Application

```
docker-compose up
```
### Testing

**POST /users - Adding User**
![image](https://github.com/orvil1026/Flask-Rest-Api/assets/58859056/6cb4e5ad-2613-4e74-a987-3917faf1b89d)
![image](https://github.com/orvil1026/Flask-Rest-Api/assets/58859056/21c62f78-109f-481d-a007-4544aa467421)

**GET /users - Returns All Users**
![image](https://github.com/orvil1026/Flask-Rest-Api/assets/58859056/b4a0ed6e-4fac-43c7-8fc8-d79a3d6a8a92)

**GET /users/<id> - Returns the user with the specified ID.** 
![image](https://github.com/orvil1026/Flask-Rest-Api/assets/58859056/d195d459-ed08-461f-ad16-6f229cc5a864)

 **PUT /users/<id> -  Updates the user**
 ![image](https://github.com/orvil1026/Flask-Rest-Api/assets/58859056/673df412-9f70-44a3-a79a-c1072eb0b332)

**DELETE /users/<id> - Deletes the user** 
![image](https://github.com/orvil1026/Flask-Rest-Api/assets/58859056/c27b8bdf-22e6-402d-9b22-915d546ca51b)

