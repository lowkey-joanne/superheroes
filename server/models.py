from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Hero Model
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade="all, delete-orphan")
    powers = db.association_proxy('hero_powers', 'power')

    serialize_rules = ('-hero_powers.hero', '-powers.hero_powers')

    def __repr__(self):
        return f"<Hero {self.name} (Alias: {self.super_name})>"

# Power Model
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='power', cascade="all, delete-orphan")
    heroes = db.association_proxy('hero_powers', 'hero')

    serialize_rules = ('-hero_powers.power', '-heroes.hero_powers')

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 15:
            raise ValueError("Description must be longer than 15 characters")
        return description

    def __repr__(self):
        return f"<Power {self.name}>"

# HeroPower Model (Join Table)
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Average', 'Weak']:
            raise ValueError("Invalid strength. Must be one of 'Strong', 'Average', or 'Weak'")
        return value

    def __repr__(self):
        return f"<HeroPower {self.hero.name} with {self.power.name} (Strength: {self.strength})>"
