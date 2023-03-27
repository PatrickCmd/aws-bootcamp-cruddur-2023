from flask import Flask, jsonify, g
from flask import request
from flask_cors import CORS, cross_origin
import os
import psycopg

# Flask AWSCognito ----------------
from utils.cognito_jwt_token import authentication_required
from flask_awscognito import AWSCognitoAuthentication

# Honeycomb ------------------
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    ConsoleSpanExporter,
)

# X-Ray -------------------
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Cloudwatch Logs --------------
import watchtower
import logging
from time import strftime

# Rollbar----------------------
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

from services.users_short import *
from services.home_activities import *
from services.notification_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *


# Configuring Logger to Use CloudWatch
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group="cruddur-backend-flask")
LOGGER.addHandler(console_handler)

LOGGER.addHandler(cw_handler)
LOGGER.info("Test CloudWatch Logs!")


# Honeycomb ------------------
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
# Processor for sending logs to honeycomb
processor = BatchSpanProcessor(OTLPSpanExporter())
# Processor for sending logs to the console (STDOUT)
simple_console_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
provider.add_span_processor(simple_console_processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)

# Flask AWSCognitov ----------------
"""
app.config['AWS_DEFAULT_REGION'] = os.getenv("AWS_DEFAULT_REGION")
app.config['AWS_COGNITO_USER_POOL_ID'] = os.getenv("AWS_COGNITO_USER_POOL_ID")
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID")
aws_auth = AWSCognitoAuthentication(app)
"""

# Honeycomb ------------------
# Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# AWS X-RAY --------------------

""" Trying to minimize spend: Comment out to enable AWS X-RAY.
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service="backend-flask", dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)
"""

# Rollbar ------------------
rollbar_access_token = os.getenv("ROLLBAR_ACCESS_TOKEN")

frontend = os.getenv("FRONTEND_URL")
backend = os.getenv("BACKEND_URL")
database_url = os.getenv("DATABASE_URL")
origins = [frontend, backend]
cors = CORS(
    app,
    resources={r"/api/*": {"origins": origins}},
    headers=["Content-Type", "Authorization"],
    expose_headers="Authorization",
    methods="OPTIONS,GET,HEAD,POST",
)
conn = psycopg.connect(database_url)


@app.after_request
def after_request(response):
    timestamp = strftime("[%Y-%b-%d %H:%M]")
    LOGGER.error(
        "%s %s %s %s %s %s",
        timestamp,
        request.remote_addr,
        request.method,
        request.scheme,
        request.full_path,
        response.status,
    )
    return response


# Rollbar ----------------------------------
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
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


@app.route("/rollbar/test")
def rollbar_test():
    rollbar.report_message("Rollbar Testing!", "warning")
    return "Rollbar Testing!"


@app.route("/api/healthcheck", methods=["GET"])
def healthcheck():
    # add precise checks
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        resp = jsonify(health="healthy")
        resp.status_code = 200
    except Exception as e:
        resp = jsonify(health="unhealthy")
        resp.status_code = 500
    return resp


@app.route("/api/message_groups", methods=["GET"])
@authentication_required
def data_message_groups():
    claims = g.cognito_claims
    cognito_user_id = claims["sub"]
    current_user = g.current_user

    model = MessageGroups.run(cognito_user_id=cognito_user_id)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200


@app.route("/api/messages/<string:message_group_uuid>", methods=["GET"])
@authentication_required
def data_messages(message_group_uuid):
    claims = g.cognito_claims
    cognito_user_id = claims["sub"]
    model = Messages.run(
        cognito_user_id=cognito_user_id, message_group_uuid=message_group_uuid
    )
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


@app.route("/api/messages", methods=["POST", "OPTIONS"])
@cross_origin()
@authentication_required
def data_create_message():
    message_group_uuid = request.json.get("message_group_uuid", None)
    user_receiver_handle = request.json.get("handle", None)
    message = request.json["message"]

    claims = g.cognito_claims
    current_user = g.current_user
    cognito_user_id = claims["sub"]

    if message_group_uuid == None:
        # Create for the first time
        model = CreateMessage.run(
            mode="create",
            message=message,
            cognito_user_id=cognito_user_id,
            current_user=current_user,
            user_receiver_handle=user_receiver_handle,
        )
    else:
        # Push onto existing Message Group
        model = CreateMessage.run(
            mode="update",
            message=message,
            message_group_uuid=message_group_uuid,
            cognito_user_id=cognito_user_id,
            current_user=current_user,
        )

    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200


@app.route("/api/activities/home", methods=["GET"])
def data_home():
    # Todo: Remove this try exception block
    try:
        # claims = cognito_jwt_token.verify(access_token)
        claims = g.cognito_claims
        # authenicatied request
        data = HomeActivities.run(logger=LOGGER, cognito_user_id=claims["username"])
    except AttributeError as e:
        # unauthenicatied request
        app.logger.debug(e)
        data = HomeActivities.run(logger=LOGGER)
    return data, 200


@app.route("/api/activities/notifications", methods=["GET"])
@authentication_required
def data_notifications():
    data = NotificationActivities.run()
    return data, 200


@app.route("/api/activities/@<string:handle>", methods=["GET"])
@authentication_required
def data_handle(handle):
    model = UserActivities.run(handle)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200


@app.route("/api/activities/search", methods=["GET"])
@authentication_required
def data_search():
    term = request.args.get("term")
    model = SearchActivities.run(term)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


@app.route("/api/activities", methods=["POST", "OPTIONS"])
@cross_origin()
@authentication_required
def data_activities():
    current_user = g.current_user

    user_handle = current_user.get("preferred_username")
    message = request.json["message"]
    ttl = request.json["ttl"]
    model = CreateActivity.run(message, user_handle, ttl)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


@app.route("/api/activities/<string:activity_uuid>", methods=["GET"])
@authentication_required
def data_show_activity(activity_uuid):
    data = ShowActivity.run(activity_uuid=activity_uuid)
    return data, 200


@app.route("/api/activities/<string:activity_uuid>/reply", methods=["POST", "OPTIONS"])
@cross_origin()
@authentication_required
def data_activities_reply(activity_uuid):
    current_user = g.current_user
    user_handle = current_user.get("preferred_username")
    message = request.json["message"]
    ttl = request.json["ttl"]
    model = CreateReply.run(message, user_handle, ttl)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200


@app.route("/api/users/@<string:handle>/short", methods=["GET"])
def data_users_short(handle):
    data = UsersShort.run(handle)
    return data, 200


if __name__ == "__main__":
    app.run(debug=True)
