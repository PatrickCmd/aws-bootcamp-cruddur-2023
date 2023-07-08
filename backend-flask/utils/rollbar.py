import os
from time import strftime

import rollbar
import rollbar.contrib.flask
from flask import current_app as app
from flask import got_request_exception


def init_rollbar():
    rollbar_access_token = os.getenv("ROLLBAR_ACCESS_TOKEN")
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        "production",
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False,
    )
    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
    return rollbar