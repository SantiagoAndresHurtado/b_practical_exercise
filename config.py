"""
Here is the main modules configuration.
"""

# 3rd party modules
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import connexion            # It uses Flask

# Local modules
from lib import routes


# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=routes.rootFolder)

# Get the underlying Flask app instance
app = connex_app.app

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_ECHO'] = False           # put False for production deployment
app.config['SQLALCHEMY_DATABASE_URI'] = routes.databaseFile
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)
