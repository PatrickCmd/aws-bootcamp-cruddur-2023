from aws_xray_sdk.core import xray_recorder
from flask import g, request
from flask_cors import cross_origin
from services.create_message import CreateMessage
from services.message_groups import MessageGroups
from services.messages import Messages
from utils.cognito_jwt_token import authentication_required
from utils.helpers import model_json


def load(app, LOGGER):
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
