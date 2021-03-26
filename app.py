"""
Main module to activate web service.
"""

# 3rd party modules
import logging.config
import logging
from flask import render_template
from flask_cors import CORS
from waitress import serve

# Local modules
from lib import routes, db_controller
import config

logging.config.fileConfig(fname=routes.loggingFile, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = config.connex_app         # Read the swagger.yml file to configure the endpoints
app.add_api(routes.swaggerFile, options={"swagger_ui": True})
CORS(app.app)


@app.route("/")
def home():
    """
    This function responds to the browser URL http://localhost:2222/
    :return:        the rendered template "home.html"
    """
    users = db_controller.search_user()
    names = [user.name for user in users]
    logger.info('home page')
    return render_template("home.html", contacts = names)


if __name__ == '__main__':
    logger.info('----------------------------------------------------------------------------')
    logger.info('Server is running')
    serve(app, listen='*:2222', ident='Beitech Server')
    # app.run(host='0.0.0.0', port=2222, debug=True)
