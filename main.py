from flask import Flask, request
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
# TODO: create unfinished APIs, use builder concept, apply validation, breakdown into different files, remove unncessary comments
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
        return {"message": "username or password incorrect"}
    correct = pbkdf2_sha256.verify(user['password'], hash)
    if correct:
        accessToken = generate_access_token(user['_id'])
        refreshToken = generate_refresh_token(user['_id'])
        return {"message": "login success", "accessToken": accessToken, "refreshToken": refreshToken}, 200
    else:
        return {"message": "username or password incorrect"}
    

# item API
@app.route("/api/v1/items", methods=['GET'])
def getItems():
    records = item_table.find()
    json_data = dumps(list(records), indent=2)
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
@app.route("/api/v1/menu", methods=['GET'])
def getMenus():
    menus = menu_table.find()
    json_data = dumps(list(menus), indent=2)
    return json_data, 200

@app.route("/api/v1/menu", methods=['POST'])
def createMenu():
    payload = request.get_json()
    newMenu = menu_table.insert_one(payload)
    return {"message": "menu created with id " + str(newMenu.inserted_id)}, 200

@app.route("/api/v1/menu", methods=['PUT'])
def updateMenu():
    payload = request.get_json()
    menu_table.update_one({"_id": request.get_json()["_id"]}, {"$set": payload})
    return {"message": "item updated"}, 200

@app.route("/api/v1/menu/<menu_id>", methods=['DELETE'])
def deleteMenu(menu_id):
    menu_table.delete_one({ '_id': menu_id })
    return {"message": "delete success"}, 200


# @app.route("/records", methods=['GET', 'POST', 'PUT', 'DELETE'])
# def getRecords():
#     if request.method == 'GET':
#         records = item_table.find()
#         json_data = dumps(list(records), indent=2)
#         return json_data

#     elif request.method == 'POST':
#         # payload = loads(dumps(request.form))
#         print(request.get_json()["_id"])
#         payload = loads(request.get_json())
#         item_id = item_table.insert_one(payload)
#         return {"message": "item created with id " + str(item_id.inserted_id)}
    
#     elif request.method == 'DELETE':
#         print(item_id)
#         item_table.delete_one({ 'id_': item_id })
#         return {"message": "delete success"}

if __name__ == "__main__":
	app.run(debug=True)

# names = {
#     "jacky": {"age": 19, "gender": "male"},
#     "bill": {"age": 70, "gender": "male"}
# }

# video_put_args = reqparse.RequestParser()
# video_put_args.add_argument("name", type=str, help="name cannot be null", required=True)
# video_put_args.add_argument("likes", type=int, help="likes cannot be null", required=True)
# video_put_args.add_argument("views", type=int, help="views cannot be null", required=True)

# videos = {}

# def abort_if_video_doesnt_exist(video_id):
#     if int(video_id) not in videos:
#         abort(404, message="Video_id does not exist")

# def abort_if_video_exists(video_id):
#     if int(video_id) in videos:
#         abort(409, message="Video_id already exist")

# class Video(Resource):
#     def get(self, video_id):
#         abort_if_video_doesnt_exist(video_id)
#         return videos[int(video_id)]
    
#     # body: likes, name, views
#     def post(self, video_id):
#         abort_if_video_exists(video_id)
#         args = video_put_args.parse_args()
#         videos[int(video_id)] = args
#         return videos[int(video_id)]

#     def delete(self, video_id):
#         abort_if_video_doesnt_exist(video_id)
#         del videos[int(video_id)]
#         return {"message": "video deleted"}, 201

# class HelloWorld(Resource):
#     def get(self, name):
#         return {"data": "Hello World!", "name": names[name]}

# api.add_resource(HelloWorld, "/helloworld/<name>")

# api.add_resource(Video, "/video/<video_id>")