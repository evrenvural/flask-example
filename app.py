from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": f"An item with name '{name}' is already exists."}, 400
        data = request.get_json(force=True)
        item = {"name": name, "price": data["price"]}
        items.append(item)

        return item, 201


class ItemList(Resource):
    def get(self):
        return items


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/item/all")


app.run(debug=True)
