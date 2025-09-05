# type: ignore
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql.expression import func
from sqlalchemy import text, Index
from config import get_config
from werkzeug.security import generate_password_hash

from dotenv import load_dotenv


load_dotenv()

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def Create_app(config_name='development'):

    app = Flask(__name__)
    config_class = get_config(config_name)
    config_class.init_app(app)


    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)



    from .tech import tech as tech_blueprint
    app.register_blueprint(tech_blueprint)

    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("All tables created successfully.")
        create_daemon_tech_user()
        app.run(debug=True)

    return app


def create_daemon_tech_user():
    from app.models import UserLogin
    daemon_user = UserLogin.query.filter_by(user_name='daemon_tech').first()
    
    if not daemon_user:
        new_user = UserLogin( 
            user_name='daemon_tech',
            password_hash=generate_password_hash('daemon_tech_password'),            
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        print("Daemon tech user created successfully.")
    else:
        print("Daemon tech user already exists.")
        
