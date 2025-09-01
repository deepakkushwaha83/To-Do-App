#Importing Flask framework and SQLAlchemy ORM (Object Relational Mapper) to interact with the database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#create database object globally
# Creates a global db object that can be used across the app.
# Notice: db is not linked to any Flask app yet. It will be linked later inside create_app()
db = SQLAlchemy()           


# This is the application factory function.
# Instead of creating the Flask app globally, you create it inside a function.
# Benefit: You can create multiple app instances with different settings (useful for testing, dev, production).
def create_app():           
    app = Flask(__name__)   #create a flask object, this can be called as engine of the app
        
    app.config['SECRET_KEY']="my-secret-key"                    #Needed for session cookies and security. 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'    #Defines which database to use (here it's a SQLite file called todo.db) 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False          #set as False to avoid warning.(Disabled to save memory (it’s deprecated warning if kept True)



    # Binds the previously created db object with this Flask app instance.Now models can use this db.
    db.init_app(app)       



    # Importing Blueprints (auth_bp and task_bp) from routes folder.
    # Blueprint is like a mini-app inside Flask, which keeps routes organized.
    # Registering them with the app
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app  #Finally returns the Flask app instance so you can run it.