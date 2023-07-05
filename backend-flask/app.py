import os

import psycopg
from flask import Flask, g, jsonify, request
from flask_cors import CORS, cross_origin
from services.create_activity import *
from services.create_message import *
from services.create_reply import *
from services.home_activities import *
from services.message_groups import *
from services.messages import *
from services.notification_activities import *
from services.search_activities import *
from services.show_activity import *
from services.update_profile import *
from services.user_activities import *
from services.users_short import *
from utils.cloudwatch import init_cloudwatch
from utils.cognito_jwt_token import authentication_required
from utils.cors import init_cors
from utils.honeycomb import init_honeycomb
from utils.logging_config import configure_logging
from utils.rollbar import init_rollbar as rollbar
from utils.xray import init_xray

# Configuring Logger
LOGGER = configure_logging()

app = Flask(__name__)

# Honeycomb
init_honeycomb(app)

# AWS X-RAY
init_xray(app)

# CORS
init_cors(app)
database_url = os.getenv("DATABASE_URL")
conn = psycopg.connect(database_url)


def model_json(model):
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200


@app.after_request
def after_request(response):
    init_cloudwatch(response, LOGGER)
    return response


# Rollbar
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar()


@app.route("/rollbar/test")
def rollbar_test():
    rollbar().report_message("Rollbar Testing!", "warning")
    return "Rollbar Testing!"


@app.route("/api/health-check")
def health_check():
    return {"success": True}, 200


@app.route("/api/message_groups", methods=["GET"])
@authentication_required
def data_message_groups():
    claims = g.cognito_claims
    cognito_user_id = claims["sub"]
    current_user = g.current_user

    model = MessageGroups.run(cognito_user_id=cognito_user_id)
    return model_json(model)


@app.route("/api/messages/<string:message_group_uuid>", methods=["GET"])
@authentication_required
def data_messages(message_group_uuid):
    claims = g.cognito_claims
    cognito_user_id = claims["sub"]
    model = Messages.run(
        cognito_user_id=cognito_user_id, message_group_uuid=message_group_uuid
    )
    return model_json(model)


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

    return model_json(model)


def default_home_feed(e):
    # unauthenicatied request
    app.logger.debug(e)
    app.logger.debug("unauthenicated")
    data = HomeActivities.run(logger=LOGGER)
    return data, 200


@app.route("/api/activities/home", methods=["GET"])
@authentication_required(on_error=default_home_feed)
def data_home():
    claims = g.cognito_claims
    data = HomeActivities.run(logger=LOGGER, cognito_user_id=claims["username"])
    return data, 200


@app.route("/api/activities/notifications", methods=["GET"])
def data_notifications():
    data = NotificationActivities.run()
    return data, 200


@app.route("/api/activities/@<string:handle>", methods=["GET"])
def data_handle(handle):
    model = UserActivities.run(handle)
    return model_json(model)


@app.route("/api/activities/search", methods=["GET"])
def data_search():
    term = request.args.get("term")
    model = SearchActivities.run(term)
    return model_json(model)


@app.route("/api/activities", methods=["POST", "OPTIONS"])
@cross_origin()
@authentication_required
def data_activities():
    current_user = g.current_user

    user_handle = current_user.get("preferred_username")
    message = request.json["message"]
    ttl = request.json["ttl"]
    model = CreateActivity.run(message, user_handle, ttl)
    return model_json(model)


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
    return model_json(model)


@app.route("/api/users/@<string:handle>/short", methods=["GET"])
def data_users_short(handle):
    """Get user profile details"""
    data = UsersShort.run(handle)
    return data, 200


@app.route("/api/profile/update", methods=["POST", "OPTIONS"])
@cross_origin()
@authentication_required
def data_update_profile():
    bio = request.json.get("bio", None)
    display_name = request.json.get("display_name", None)

    claims = g.cognito_claims
    cognito_user_id = claims["sub"]

    model = UpdateProfile.run(
        cognito_user_id=cognito_user_id, bio=bio, display_name=display_name
    )
    return model_json(model)


if __name__ == "__main__":
    app.run(debug=True)
