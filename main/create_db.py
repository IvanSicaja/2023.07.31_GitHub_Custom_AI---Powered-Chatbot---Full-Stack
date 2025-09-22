import click
from backend import app, db  # Import Flask app instance and SQLAlchemy instance
from flask.cli import with_appcontext

# Create a function to create database tables
@with_appcontext
def create_database():
    db.create_all()
    print('Database is created.')

# Define a command to create the database
@click.command()
def create_db():
    with app.app_context():
        create_database()

# Add the command to the Flask CLI
app.cli.add_command(create_db)

# Run the Flask CLI
if __name__ == '__main__':
    create_db()
