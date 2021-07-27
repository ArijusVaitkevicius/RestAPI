from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app_server = Flask(__name__)
app_server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'items.db')
app_server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app_server)
ma = Marshmallow(app_server)


# DB objektas
class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String)
    price = db.Column("Price", db.Integer)
    qtty = db.Column("Quantity", db.Integer)


# Užduoties schema
class ItemsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'qtty')


item_schema = ItemsSchema()
items_schema = ItemsSchema(many=True)


# Crud
@app_server.route('/items', methods=['POST'])
def add_item():
    db.create_all()
    name = request.json['name']
    price = request.json['price']
    qtty = request.json['qtty']
    new_item = Items(name=name, price=price, qtty=qtty)
    db.session.add(new_item)
    db.session.commit()
    return item_schema.jsonify(new_item)


# cRud
@app_server.route('/items', methods=['GET'])
def get_all_items():
    all_items = Items.query.all()
    result = items_schema.dump(all_items)
    return jsonify(result)


# cRud
@app_server.route('/items/<id>', methods=['GET'])
def get_item(id):
    item = Items.query.get(id)
    return item_schema.jsonify(item)


# crUd
@app_server.route('/items/<id>', methods=['PUT'])
def edit_item(id):
    item = Items.query.get(id)
    item.name = request.json['name']
    item.price = request.json['price']
    item.qtty = request.json['qtty']
    db.session.commit()
    return item_schema.jsonify(item)


# cruD
@app_server.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    item = Items.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return item_schema.jsonify(item)


if __name__ == '__main__':
    app_server.run(host='127.0.0.1', port=5000, debug=True)
    db.create_all()
