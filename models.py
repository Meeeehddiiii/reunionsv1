# models.py
from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class Accueil(db.Model):
    __tablename__ = 'Accueil'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)

# Définissez ici les autres modèles (Estrade, Sono, Perchiste, Programme)
class Sono(db.Model):
    __tablename__ = 'Sono'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)

class Perchiste(db.Model):
    __tablename__ = 'Perchiste'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)

class Estrade(db.Model):
    __tablename__ = 'Estrade'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)