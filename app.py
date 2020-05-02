from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": f"An item with name '{name}' is already exists."}, 400

        data = self.parser.parse_args()

        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": f"item with name '{name}' deleted"}, 200

    def put(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)

        if item is None:
            return {"message": f"An item with name '{name}' is not found."}, 400

        data = self.parser.parse_args()

        item.update(data)
        return item, 200


class ItemList(Resource):
    def get(self):
        return items


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/item/all")

app.run(debug=True)
