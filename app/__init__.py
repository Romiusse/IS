from flask import Flask
from .database import init_db
import os

def create_app():
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY=os.getenv('FLASK_SECRET_KEY'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
        DATABASE_URL=os.getenv('DATABASE_URL'),
        TESTING=False
    )

    init_db(app)

    from .auth import auth_bp
    from .routes import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
