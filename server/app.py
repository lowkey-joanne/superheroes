#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower

# Configure database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route('/')
def home():
    """
    Basic route to check if the server is operational.
    """
    return '<h1>Welcome to the API</h1>'

# Error handler for 404 (Not Found)
@app.errorhandler(404)
def handle_404(error):
    return jsonify({"message": "Resource not found"}), 404

# Error handler for 500 (Internal Server Error)
@app.errorhandler(500)
def handle_500(error):
    return jsonify({"message": "Internal Server Error"}), 500

class HeroResource(Resource):
    def get(self, hero_id=None):
        """
        Handle GET requests to fetch hero details.
        """
        if hero_id:
            hero = Hero.query.get(hero_id)
            if hero:
                return jsonify(hero.to_dict())
            return jsonify({"message": "Hero not found"}), 404
        
        all_heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in all_heroes])

    def post(self):
        """
        Handle POST requests to add a new hero.
        """
        data = request.get_json()
        try:
            new_hero = Hero(name=data['name'], super_name=data['super_name'])
            db.session.add(new_hero)
            db.session.commit()
            return jsonify(new_hero.to_dict()), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 400

class PowerResource(Resource):
    def get(self, power_id=None):
        """
        Handle GET requests to fetch power details.
        """
        if power_id:
            power = Power.query.get(power_id)
            if power:
                return jsonify(power.to_dict())
            return jsonify({"message": "Power not found"}), 404
        
        all_powers = Power.query.all()
        return jsonify([power.to_dict() for power in all_powers])

    def post(self):
        """
        Handle POST requests to add a new power.
        """
        data = request.get_json()
        try:
            new_power = Power(name=data['name'], description=data['description'])
            db.session.add(new_power)
            db.session.commit()
            return jsonify(new_power.to_dict()), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 400

# Register resources with the API
api.add_resource(HeroResource, '/heroes', '/heroes/<int:hero_id>')
api.add_resource(PowerResource, '/powers', '/powers/<int:power_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
