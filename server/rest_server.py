from flask import Flask, request, jsonify
# from logic.kettle import Kettle
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__)
CORS(app)
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

    def __init__(self, title,duration,parent_id,recipe_id,manual_next):
        self.title = title
        self.duration = duration
        self.parent_id = parent_id
        self.recipe_id = recipe_id
        self.manual_next = manual_next

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Time, nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('recipestep.id'), index=True)
    childrens = db.relationship('RecipeStep', backref=db.backref('parent', remote_side='RecipeStep.id'))

    manual_next = db.column(db.Boolean)

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = db.relationship('Recipe', backref=db.backref('steps', lazy=True))


class RecipeStepSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title','duration','parent_id','recipe_id')

db.create_all()


recipes_schema = RecipeSchema(many=True)
recipe_schema = RecipeSchema()

recipes_step_schema = RecipeStepSchema(many=True)
recipe_step_schema = RecipeStepSchema()



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


@app.route("/recipes/<id>/steps", methods=["GET"])
def get_recipe_steps(id):
    steps = RecipeStep.query.filter_by(recipe_id=id)
    return jsonify(recipes_step_schema.dump(steps)), 200


@app.route("/recipes/<id>/steps/<step_id>", methods=["DELETE"])
def delete_recipe_step(id,step_id):
    item = RecipeStep.query.filter_by(id=step_id).first_or_404(f'No item with id: {id}')
    db.session.delete(item)
    db.session.commit()
    return {},200

@app.route("/recipes/<id>/steps", methods=["POST"])
def add_recipe_step():
    new_step = RecipeStep(request.json['title'], request.json['duration'], request.json['parent_id'], request.json['recipe_id'], request.json['manual_next'])
    db.session.add(new_step)
    db.session.commit()
    return recipe_step_schema.dump(new_step), 201

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')