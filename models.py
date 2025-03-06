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

class Programme(db.Model):
    __tablename__ = 'programme'
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    datePlanning = db.Column(db.Date, nullable=False)
    parking = db.Column(db.String(30))
    entree = db.Column(db.String(30))
    auditorium = db.Column(db.String(30))
    estrade = db.Column(db.String(30))
    zoom = db.Column(db.String(30))
    sono = db.Column(db.String(30))
    perchiste1 = db.Column(db.String(30))
    perchiste2 = db.Column(db.String(30))
    perchiste3 = db.Column(db.String(30))
    perchiste4 = db.Column(db.String(30))
    candidate_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<Programme {self.datePlanning}>'