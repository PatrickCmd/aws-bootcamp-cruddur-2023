from aws_xray_sdk.core import xray_recorder
from flask import g, request
from flask_cors import cross_origin
from services.show_activity import ShowActivity
from services.update_profile import UpdateProfile
from services.user_activities import UserActivities
from services.users_short import UsersShort
from utils.cognito_jwt_token import authentication_required
from utils.helpers import model_json


def load(app, LOGGER):
    @app.route("/api/activities/@<string:handle>", methods=["GET"])
    def data_users_activities(handle):
        model = UserActivities.run(handle)
        return model_json(model)

    @app.route("/api/users/@<string:handle>/short", methods=["GET"])
    def data_users_short(handle):
        """Get user profile details"""
        data = UsersShort.run(handle)
        return data, 200

    @app.route(
        "/api/activities/@<string:handle>/status/<string:activity_uuid>",
        methods=["GET"],
    )
    @xray_recorder.capture("activities_show")
    def data_show_activity(activity_uuid):
        data = ShowActivity.run(activity_uuid=activity_uuid)
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
