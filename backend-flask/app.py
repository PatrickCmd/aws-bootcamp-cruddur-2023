import os

import psycopg
import routes.activities
import routes.general
import routes.messages
import routes.users
from flask import Flask,g
from utils.cloudwatch import init_cloudwatch
from utils.cors import init_cors
from utils.helpers import model_json
from utils.honeycomb import init_honeycomb
from utils.logging_config import configure_logging
from utils.rollbar import init_rollbar
from utils.xray import init_xray

# Configuring Logger
LOGGER = configure_logging()

app = Flask(__name__)

# Honeycomb
init_honeycomb(app)
# AWS X-RAY
init_xray(app)
# Rollbar
with app.app_context():
    g.rollbar = init_rollbar(app)

# CORS
init_cors(app)
database_url = os.getenv("DATABASE_URL")
conn = psycopg.connect(database_url)


# @app.after_request
# def after_request(response):
#     init_cloudwatch(response, LOGGER)
#     return response


# load routes
routes.general.load(app)
routes.activities.load(app, LOGGER)
routes.users.load(app, LOGGER)
routes.messages.load(app, LOGGER)


if __name__ == "__main__":
    app.run(debug=True)
