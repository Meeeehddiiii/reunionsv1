# routes/__init__.py

from routes.accueil import accueil_bp
from routes.sono import sono_bp
from routes.perchiste import perchiste_bp
from routes.programme import programme_bp

def init_app(app):
    app.register_blueprint(accueil_bp)
    app.register_blueprint(sono_bp)
    app.register_blueprint(perchiste_bp)
    app.register_blueprint(programme_bp)