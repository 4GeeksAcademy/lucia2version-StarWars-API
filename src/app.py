"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Favorites, People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/people', methods=['GET'])
def get_all_people():
    all_people = People.query.all()
    people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(people), 200



@app.route('/people/<int:people_id>', methods=['GET'])
def get_each_person(id):
    people_id = People.query.filter_by(people_id = id)
    people = list(map(lambda x: x.serialize(), people_id))
    return jsonify(people_id), 200




@app.route('/planets', methods=['GET'])
def handle_hello():
    all_planets = Planets.query.all()
    planets = list(map(lambda x: x.serialize(), all_planets))
    return jsonify(planets), 200



@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets(id):
    planet_id = Planets.query.filter_by(planet_id = id)
    planets = list(map(lambda x: x.serialize(), planet_id))
    return jsonify(planet_id), 200


@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    users = list(map(lambda x: x.serialize(), all_users))
    return jsonify(users), 200



@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_user_fav(id):
    all_favorites = Favorites.query.filter_by(user_id = id)
    fav = list(map(lambda x: x.serialize(), all_favorites))
    return jsonify(fav), 200



@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorite_planet(user_id, planet_id):
    favorite = Favorites(user_id = user_id, planet_id = planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200


@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def post_favorite_people(user_id, people_id):
    favorite = Favorites(user_id = user_id, people_id = people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200



@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    planet = Favorites.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    db.session.delete(planet)
    db.session.commit()
    return jsonify("You have deleted a favorite planet")



@app.route('/favorite/people/<int:planet_id>', methods=['DELETE'])
def delete_favorite_person(user_id, people_id):
    people = Favorites.query.filter_by(user_id = user_id, people_id = people_id).first()
    db.session.delete(people)
    db.session.commit()
    return jsonify("You have deleted a favorite person")





