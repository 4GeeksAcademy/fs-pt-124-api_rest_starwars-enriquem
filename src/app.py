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
from models import db, User, Character, Race, Zone, ClassBase
from sqlalchemy import select
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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#ENDPOINTS


    # GET - race, todos
@app.route('/races', methods=['GET'])
def get_races():

    races = db.session.execute(select(Race)).scalars().all()
    print(races)
    result = []
    
    for race in races:
        result.append(race.serialize())
    
    return jsonify(result), 200


    # GET - race, por id
@app.route('/races/<int:races_id>', methods=['GET'])
def get_races_id(races_id):

    races = db.session.get(Race, races_id)

    if races is None:
        return jsonify({"msg":"Race not found"}), 404
    
    return jsonify(races.serialize()), 200


    # GET -zone, todos
@app.route('/zones', methods=['GET'])
def get_zones():

    zones = db.session.execute(select(Zone)).scalars().all()
    print(zones)
    result = []
    
    for zone in zones:
        result.append(zone.serialize())
    
    return jsonify(result), 200
    
    
    # GET - zone,  por id
@app.route('/zones/<int:zone_id>', methods=['GET'])
def get_zone_id(zone_id):

    zone = db.session.get(Zone, zone_id)

    if zone is None:
        return jsonify({"msg":"Zone not found"}), 404
    
    return jsonify(zone.serialize()), 200

# GET - user, todos
@app.route('/users', methods=['GET'])
def get_users():

    users = db.session.execute(select(User)).scalars().all()
    result = []
    for user in users:
        result.append(user.serialize())
    return jsonify(result), 200

# GET - user, por id
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({"msg":"User not found"}), 404
    
    return jsonify(user.serialize()), 200

# GET - character, por todos
@app.route('/characters', methods=['GET'])
def get_characters():

    characters = db.session.execute(select(Character)).scalars().all()
    result = []
    for character in characters:
        result.append(character.serialize())
    return jsonify(result), 200
    

# GET - character, por id
@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = db.session.execute(select(Character).where(Character.id == character_id)).scalar_one_or_none()
    print(db.engine.url)
    if character is None:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(character.serialize()), 200

    # PUT - agregar raza a un personaje
@app.route('/characters/<int:character_id>/races/<int:race_id>', methods=['PUT'])
def edit_race_to_character(character_id, race_id):

    character = Character.query.get(character_id)
    if not character:
        return {"msg": "Character not found"}, 404
    
    race = Race.query.get(race_id)
    if not race:
        return {"msg", "Race not found"}, 404
    
    if character.race_choice_id == race_id:
        return {"msg": "Character already has this race"}, 400
    
    character.race_choice_id = race_id

    db.session.commit()

    return {"msg": "Race assigned to character"}, 200

    # GET - clase base

@app.route('/class_bases', methods=['GET'])
def get_class_bases():

    class_bases = db.session.execute(select(ClassBase)).scalars().all()
    print(class_bases)
    result = []
    
    for class_base in class_bases:
        result.append(class_base.serialize())
    
    return jsonify(result), 200

    # PUT - agregar clase base a un personaje

@app.route('/characters/<int:character_id>/class_base/<int:class_base_id>', methods=['PUT'])
def edit_class_base_to_character(character_id, class_base_id):

    character = Character.query.get(character_id)
    if not character:
        return {"msg": "Character not found"}, 404
    
    class_base = ClassBase.query.get(class_base_id)
    if not class_base:
        return {"msg", "Class base not found"}, 404
    
    if character.class_base_choice_id == class_base_id:
        return {"msg": "Character already has this class"}, 400
    
    character.class_base_choice_id = class_base_id

    db.session.commit()

    return {"msg": "Class assigned to character"}, 200
    
    
    # DELETE - quitar raza a un personaje
@app.route('/characters/<int:character_id>/races/<int:race_id>', methods=['DELETE'])
def delete_race_relation(character_id, race_id):

    relation = Character.query.filter_by(
        id=character_id,
        race_choice_id=race_id
    ).first()

    if not relation:
        return jsonify({"msg": "Relation nor found"}), 400
    
    relation.race_choice_id = None
    db.session.commit()

    return jsonify({"msg": "Relation deleted"}), 200


    # DELETE - quitar clase base a un personaje
@app.route('/characters/<int:character_id>/class_base/<int:class_base_id>', methods=['DELETE'])
def delete_class_base_relation(character_id, class_base_id):

    relation = Character.query.filter_by(
        id=character_id,
        class_base_choice_id=class_base_id
    ).first()

    if not relation:
        return jsonify({"msg": "Relation not found"}), 400
    
    relation.class_base_choice_id = None
    db.session.commit()

    return jsonify({"msg": "Relation deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)