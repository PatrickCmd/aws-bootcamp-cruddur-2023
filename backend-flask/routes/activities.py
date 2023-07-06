from aws_xray_sdk.core import xray_recorder
from flask import g, request
from flask_cors import cross_origin
from services.create_activity import *
from services.create_reply import *
from services.home_activities import *
from services.notification_activities import *
from services.search_activities import *
from services.show_activity import *
from utils.cognito_jwt_token import authentication_required
from utils.helpers import model_json


def load(app, LOGGER):
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
    @xray_recorder.capture("activities_show")
    def data_show_activity(activity_uuid):
        data = ShowActivity.run(activity_uuid=activity_uuid)
        return data, 200

    @app.route(
        "/api/activities/<string:activity_uuid>/reply", methods=["POST", "OPTIONS"]
    )
    @cross_origin()
    @authentication_required
    def data_activities_reply(activity_uuid):
        current_user = g.current_user
        user_handle = current_user.get("preferred_username")
        message = request.json["message"]
        model = CreateReply.run(message, user_handle, activity_uuid)
        return model_json(model)
