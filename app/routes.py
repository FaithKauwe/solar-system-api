from flask import Blueprint, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from app.Models.planets import Planet
from app import db

planets_bp = Blueprint('planets',__name__, url_prefix='/planets')
# defining class planet
# class Planet:
#     def __init__(self,id, name, description, number_of_moons):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.number_of_moons = number_of_moons
# data set for Planet objects
# planets = [
#             Planet(1,'Earth', 'water planet', 1), 
#             Planet(2, 'Mercury', 'fastest', 0),
#             Planet(3, 'Jupiter', 'biggest', 79),
#             Planet(4, 'Saturn', 'gaseous', 82),
#             Planet(5, 'Mars', 'red', 2),
#             Planet(6, 'Uranus', 'coldest', 27),
#             Planet(7, 'Neptune', 'farthest from the sun', 14),
#             Planet(8, 'Venus', 'hottest', 0)
#           ]

# planets_bp is a Blueprint object
#@planets_bp.route('', methods=['GET'])
# this function is to allow a user to access all planets info from a db that is hard coded into the program
def handle_planets_with_hardcode_data():
  planets_response = []
  for planet in planets:
    planets_response.append({'id': planet.id, 'name':planet.name, 
    'description':planet.description, 'number of moons': planet.number_of_moons})
  return jsonify(planets_response)
# this function allows a user to create a planet or access all planets
# using SQLAlchemey and a database connection (not hard coded)
@planets_bp.route('', methods=['POST', 'GET'])
def user_creates_new_planet_reads_all_planets():
    if request.method == "GET":
    # this SQLAlchemy syntax tells Planet to query for all() planets. This method returns a list of instances of Planet. 
      planets = Planet.query.all()
      planets_response = []
    # looping through list of planet objects and adding formatted data into planets_response list
    # planets_response will be a list of dicts 
      for planet in planets:
        planets_response.append({
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "number_of_moons": planet.number_of_moons
            })
      return jsonify(planets_response)
    # if user wants to add a new planet to DB, execute following lines
    elif request.method == "POST":
      request_body = request.get_json()
      new_planet = Planet(name=request_body["name"],
                        description=request_body["description"],
                        number_of_moons=request_body["number_of_moons"])

      db.session.add(new_planet)
      db.session.commit()

      return make_response(f"Planet {new_planet.name} successfully created", 201)
  


@planets_bp.route('/<planet_id>', methods=['GET', 'PUT', 'DELETE'])
# this function  is to allow a user to access just one planet's info, given the planet id
# using the query method of SQLAlchemy
def handle_one_planet(planet_id):
  planet = Planet.query.get(planet_id)
  if request.method == "GET":
    return {
      "id": planet.id,
      "name": planet.name,
      "description": planet.description,
      "number_of_moons": planet.number_of_moons

    }
  # this block of code is to update an existing record
  elif request.method == "PUT":
  # form data is a local variable to hold the body of the HTTP request
    form_data = request.get_json()
    planet.name = form_data['name']
    planet.description = form_data['description']
    planet.number_of_moons = form_data['number_of_moons']
  # use session.commit method of db (which is our instance of SQLAlchemy class) to save 
  # changes to db
    db.session.commit()
    return make_response(f"Planet #{planet.id} successfully updated")
# this block of code is to delete one record
  elif request.method == "DELETE":
    db.session.delete(planet)
    db.session.commit()
    return make_response(f"Planet #{planet.id} successfully deleted")




# this function  is to allow a user to access just one planet's info, given the planet id
def handle_planet(planet_id):
  planet_id = int(planet_id)
  for planet in planets:
    if planet.id == planet_id:
      return {'id': planet.id, 'name':planet.name, 
    'description':planet.description, 'number of moons': planet.number_of_moons}

# Accessing data from French solar system API
# Using blueprint decorator to let client access 'planet/bodies' endpoint
@planets_bp.route('/bodies', methods=['GET'])
# This function indicates that the content is not hardcoded and not available in localhost.
# This function uses requests package to access a different URL
def get_bodies_from_solar():
  path = 'https://api.le-systeme-solaire.net/rest/bodies/'
  query_params = {
          "filter": [isPlanet,neq,False],
          "format": "json"
      }
  response = requests.get(path, params=query_params)
  response_body = response.json()
      