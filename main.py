from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort
import pymongo
from bson.json_util import dumps, loads
from passlib.hash import pbkdf2_sha256
import jwt
import datetime

SECRET_KEY = "\x190\x8f\xe6 \x07\xcf\xc7\xb3@\x02\xfd\x17\x7f \x98\xe1\x83|\x8c|\xde\xd5B"

app = Flask(__name__)
api = Api(app)
client = pymongo.MongoClient("mongodb+srv://yiptsunho:JAn3ebgbGLrTX46r@order.os3j64k.mongodb.net/?retryWrites=true&w=majority")

myDb = client["order-menu"]
item_table = myDb["item"]
user_table = myDb['user']
menu_table = myDb['menu']
# TODO:
#  apply validation,
#  breakdown into different files,
#  remove unnecessary comments

# Authentication decorator
def login_required(f):
    
    def decorator(*args, ** kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return {'message': 'Unauthorized access'}, 401
        try:
            valid = validate_token(token)
        except:
            return {'message': 'Unauthorized access'}, 401

    return decorator

def generate_access_token(_id):
    payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': _id
        }
    return jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')

def generate_refresh_token(_id):
    payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
            'iat': datetime.datetime.utcnow(),
            'sub': _id
        }
    return jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')

def validate_token(token):
    try:
        payload = jwt.decode(token, 'SECRET_KEY')
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Expired'
    except jwt.InvalidTokenError:
        return 'Invalid'

# user API
@app.route("/api/v1/login", methods=['POST'])
def login():
    user = {
        "_id": request.get_json()['username'],
        "password": request.get_json()['password']
    }
    userExists = user_table.find_one(user['_id'])
    if userExists:
        hash = userExists['password']
    else:
        return {"message": "username or password incorrect"}, 400
    correct = pbkdf2_sha256.verify(user['password'], hash)
    if correct:
        accessToken = generate_access_token(user['_id'])
        refreshToken = generate_refresh_token(user['_id'])
        return {"message": "login success", "accessToken": accessToken, "refreshToken": refreshToken}, 200
    else:
        return {"message": "username or password incorrect"}, 400

@app.route("/api/v1/refreshSession", methods=['POST'])
def refreshSession():
    return {"message": "refreshing"}

# item API
@app.route("/api/v1/items", methods=['GET'])
# @login_required
def getAllItems():
    records = item_table.find()
    json_data = jsonify(list(records))
    return json_data, 200

@app.route("/api/v1/items/<item_id>", methods=['GET'])
@login_required
def getItem(item_id):
    records = item_table.find_one(item_id)
    json_data = jsonify(records)
    return json_data, 200

@app.route("/api/v1/items", methods=['POST'])
def createItem():
    payload = request.get_json()
    newItem = item_table.insert_one(payload)
    return {"message": "item created with id " + str(newItem.inserted_id)}, 200

@app.route("/api/v1/items", methods=['PUT'])
def updateItem():
    payload = request.get_json()
    item_table.update_one({"_id": request.get_json()["_id"]}, {"$set": payload})
    return {"message": "item updated"}, 200

@app.route("/api/v1/items/<item_id>", methods=['DELETE'])
def deleteItem(item_id):
    item_table.delete_one({ '_id': item_id })
    return {"message": "delete success"}, 200

# menu API
@app.route("/api/v1/menus", methods=['GET'])
def getMenus():
    menus = menu_table.find()
    json_data = jsonify(list(menus))
    return json_data, 200

@app.route("/api/v1/menus", methods=['POST'])
def createMenu():
    payload = request.get_json()
    newMenu = menu_table.insert_one(payload)
    return {"message": "menu created with id " + str(newMenu.inserted_id)}, 200

@app.route("/api/v1/menus", methods=['PUT'])
def updateMenu():
    payload = request.get_json()
    menu_table.update_one({"_id": request.get_json()["_id"]}, {"$set": payload})
    return {"message": "item updated"}, 200

@app.route("/api/v1/menus/<menu_id>", methods=['DELETE'])
def deleteMenu(menu_id):
    menu_table.delete_one({ '_id': menu_id })
    return {"message": "delete success"}, 200

if __name__ == "__main__":
	app.run(debug=True)
