from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

def serialize(self):
       query_people = People.query.filter_by(id=self.people_id).first()
       query_planets = Planets.query.filter_by(id=self.planet_id).first()
       return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_name": query_planets.serialize()["name"] if query_planets else None,
            "people_name": query_people.serialize()["name"] if query_people else None
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    favorite_character = db.relationship('Favorites')
  
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    mass = db.Column(db.String(250), nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    population = db.Column(db.String(250), nullable=True)
    diameter = db.Column(db.String(250), nullable=True)
    gravity = db.Column(db.String(250), nullable=True)


    favorite_planet = db.relationship('Favorites')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            "climate": self.climate,
            "population": self.population,
            "diameter": self.diameter,
            "gravity": self.gravity
        }