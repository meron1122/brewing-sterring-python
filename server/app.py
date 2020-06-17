#!/usr/bin/python
import json
import os
from flask import Flask, request, jsonify
# from logic.kettle import Kettle
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'recipes.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False)

    def __init__(self, name):
        self.name = name


class RecipeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class RecipeStep(db.Model):
    __tablename__ = 'recipestep'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Time, nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('recipestep.id'), index=True)
    sub_regions = db.relationship('RecipeStep', backref=db.backref('parent', remote_side='RecipeStep.id'))

    manual_next = db.column(db.Boolean)

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = db.relationship('Recipe', backref=db.backref('steps', lazy=True))


class RecipeStepSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title','duration','parent_id','recipe_id')

db.create_all()


recipes_schema = RecipeSchema(many=True)
recipe_schema = RecipeSchema()


@app.route("/recipes", methods=["GET"])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify(recipes_schema.dump(recipes)), 200


@app.route("/recipes/<id>", methods=["DELETE"])
def delete_recipe(id):
    item = Recipe.query.filter_by(id=id).first_or_404(f'No item with id: {id}')
    db.session.delete(item)
    db.session.commit()
    return {},200

@app.route("/recipes", methods=["POST"])
def add_recipe():
    new_recipe = Recipe(request.json['name'])
    db.session.add(new_recipe)
    db.session.commit()
    return recipe_schema.dump(new_recipe), 201


with open('appsettings.json') as f:
    settings = json.load(f)

# kettle = Kettle(int(settings['kettle']['heater_pin']), int(settings['kettle']['paddle_pin']))
#
#
# async def handler(websocket, path):
#     while 1:
#         try:
#             message = json.loads(await websocket.recv())
#             if message["command"] == "set_setpoint":
#                 kettle.set_setpoint(float(message["arg"]))
#             if message["command"] == "set_paddle":
#                 kettle.set_paddle(bool(message["arg"]))
#             if message["command"] == "emergency_stop":
#                 kettle.emergency_stop()
#
#             status = json.dumps({"temperature": str(kettle.temp), "setpoint": str(kettle.get_setpoint()),
#                                  "paddle": str(kettle.get_paddle())})
#             await websocket.send(status)
#             await asyncio.sleep(0.05)
#         except websockets.ConnectionClosed:  # bad solution :<
#             break
#
#
# start_server = websockets.serve(handler, settings['websockets']['ip'], int(settings['websockets']['port']))
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    app.run(debug=True)
