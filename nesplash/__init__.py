import os
import click
from flask import Flask, render_template, redirect, url_for

from nesplash.config import config
from nesplash.models import Role, Category, Method
from nesplash.admin.routes import admin_bp
from nesplash.main.routes import main_bp
from nesplash.user.routes import user_bp
from nesplash.auth.routes import auth_bp
from nesplash.category.foodie.routes import foodie_bp
from nesplash.category.nature.routes import nature_bp
from nesplash.category.architecture.routes import architecture_bp
from nesplash.category.travel.routes import travel_bp
from nesplash.category.athletics.routes import athletics_bp
from nesplash.category.people.routes import people_bp
from nesplash.extensions import db, ma, cors, mail, oauth

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask('nesplash')
    app.config.from_object(config[config_name])

    @app.route("/people")
    def people():
        return render_template('category/people.html')

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_errorHandler(app)
    return app

def register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(foodie_bp)
    app.register_blueprint(nature_bp)
    app.register_blueprint(architecture_bp)
    app.register_blueprint(travel_bp)
    app.register_blueprint(athletics_bp)
    app.register_blueprint(people_bp)

def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)

def register_commands(app):
    
    @app.cli.command()
    @click.option("--drop", is_flag=True, help="Create after drop")
    def initdb(drop):
        """Initialize database"""
        if drop:
            click.confirm("This operation will delete the database, do you want to continue?", abort=True)
            click.echo("Drop Table.")
            db.drop_all()
        db.create_all()
        click.echo("Initialize database")

    @app.cli.command()
    def forge():
        """Generate Open API data."""

        from nesplash.source import (
            create_admin,
            create_architecture, 
            create_athletics, 
            create_nature, 
            create_travel, 
            create_people, 
            create_food_drink,
            create_contributor,
            create_contributor_photos,
            create_architecture_video,
            create_athletics_video,
            create_food_drink_video,
            create_nature_video,
            create_people_video,
            create_travel_video
        )

        db.drop_all()
        db.create_all()

        click.echo('Initializing the roles and permissions...')
        Role.init_role()

        click.echo("Initialize the Categorys...")
        Category.init_category()

        click.echo("Initialize the methods...")
        Method.init_method()

        click.echo("making admin")
        create_admin()

        click.echo("making architecture's photos and users data...")
        create_architecture()

        click.echo("making athletics's photos and users data...")
        create_athletics()

        click.echo("making nature's photos and users data...")
        create_nature()

        click.echo("making travel's photos and users data...")
        create_travel()

        click.echo("making people's photos and users data...")
        create_people()

        click.echo("making food_drink's photos nad users data...")
        create_food_drink()

        click.echo("making contributor's users data...")
        create_contributor()

        click.echo("making contributor's photos data...")
        create_contributor_photos()

        click.echo("making architecture's videos data...")
        create_architecture_video()

        click.echo("making athletics's videos data...")
        create_athletics_video()

        click.echo("making food_drink's videos data...")
        create_food_drink_video()

        click.echo("making nature's videos data...")
        create_nature_video()

        click.echo("making people's videos data...")
        create_people_video()

        click.echo("making travel's videos data...")
        create_travel_video()
        
        click.echo("Done.")
                
def register_errorHandler(app):

    @app.errorhandler(400)
    def bad_request(e):
        return render_template("errors/400.html"), 400

    @app.errorhandler(403)
    def forbidden(e):
        return redirect(url_for("main.index"))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500
