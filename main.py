from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
import pymongo
from bson.json_util import dumps, loads

app = Flask(__name__)
api = Api(app)
client = pymongo.MongoClient("mongodb+srv://yiptsunho:JAn3ebgbGLrTX46r@order.os3j64k.mongodb.net/?retryWrites=true&w=majority")

myDb = client["order-menu"]
item_table = myDb["item"]

# user API
# @app.route("/login", methods=['POST'])
# def login():
    # print(request.get_json()["_id"])
    # payload = request.get_json()
    # item_id = item_table.insert_one(payload)
    # return {"message": "item created with id " + str(item_id.inserted_id)}
    # return {"message": request.get_json()}

# item API
@app.route("/items", methods=['GET'])
def getItems():
    records = item_table.find()
    json_data = dumps(list(records), indent=2)
    return json_data

@app.route("/items", methods=['POST'])
def createItem():
    print(request.get_json()["_id"])
    payload = request.get_json()
    item_id = item_table.insert_one(payload)
    return {"message": "item created with id " + str(item_id.inserted_id)}
    return {"message": request.get_json()}

@app.route("/items", methods=['PUT'])
def updateItem():
    print(request.get_json()["_id"])
    payload = request.get_json()
    item_id = item_table.update_one({"_id": request.get_json()["_id"]}, {"$set": payload})
    return {"message": "item updated"}

@app.route("/items/<item_id>", methods=['DELETE'])
def deleteItem(item_id):
    print(item_id)
    item_id = item_table.delete_one({ '_id': item_id })
    return {"message": "delete success"}

# menu API



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