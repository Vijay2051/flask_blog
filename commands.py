import click
from flask.cli import with_appcontext

from blog_flask import db
from blog_flask.models import Post, User

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()