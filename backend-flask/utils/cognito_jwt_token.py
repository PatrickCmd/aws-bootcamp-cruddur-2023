import json
import os
import time
from functools import partial, wraps

import boto3
import requests
from flask import abort, current_app, g, jsonify, make_response, request
from jose import jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode
from utils.exceptions import FlaskAWSCognitoError, TokenVerifyError


def extract_access_token(request_headers):
    access_token = None
    auth_header = request_headers.get("Authorization")
    if auth_header and " " in auth_header:
        _, access_token = auth_header.split()
    return access_token


def extract_current_user(request_headers):
    current_user = request_headers.get("CurrentUser")
    return json.loads(current_user)


class CognitoJwtToken:
    def __init__(self, user_pool_id, user_pool_client_id, region, request_client=None):
        self.region = region
        if not self.region:
            raise FlaskAWSCognitoError("No AWS region provided")
        self.user_pool_id = user_pool_id
        self.user_pool_client_id = user_pool_client_id
        self.claims = None
        if not request_client:
            self.request_client = requests.get
        else:
            self.request_client = request_client
        self._load_jwk_keys()

    def _load_jwk_keys(self):
        keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        try:
            response = self.request_client(keys_url)
            self.jwk_keys = response.json()["keys"]
        except requests.exceptions.RequestException as e:
            raise FlaskAWSCognitoError(str(e)) from e

    @staticmethod
    def _extract_headers(token):
        try:
            headers = jwt.get_unverified_headers(token)
            return headers
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    def _find_pkey(self, headers):
        kid = headers["kid"]
        # search for the kid in the downloaded public keys
        key_index = -1
        for i in range(len(self.jwk_keys)):
            if kid == self.jwk_keys[i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            raise TokenVerifyError("Public key not found in jwks.json")
        return self.jwk_keys[key_index]

    @staticmethod
    def _verify_signature(token, pkey_data):
        try:
            # construct the public key
            public_key = jwk.construct(pkey_data)
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e
        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(token).rsplit(".", 1)
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise TokenVerifyError("Signature verification failed")

    @staticmethod
    def _extract_claims(token):
        try:
            claims = jwt.get_unverified_claims(token)
            return claims
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    @staticmethod
    def _check_expiration(claims, current_time):
        if not current_time:
            current_time = time.time()
        if current_time > claims["exp"]:
            raise TokenVerifyError("Token is expired")  # probably another exception

    def _check_audience(self, claims):
        # and the Audience  (use claims['client_id'] if verifying an access token)
        audience = claims["aud"] if "aud" in claims else claims["client_id"]
        if audience != self.user_pool_client_id:
            raise TokenVerifyError("Token was not issued for this audience")

    def verify(self, token, current_time=None):
        """https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py"""
        if not token:
            raise TokenVerifyError("No token provided")

        headers = self._extract_headers(token)
        pkey_data = self._find_pkey(headers)
        self._verify_signature(token, pkey_data)

        claims = self._extract_claims(token)
        self._check_expiration(claims, current_time)
        self._check_audience(claims)

        self.claims = claims
        return self.claims

    # Get user info for cognito user from the access token
    def get_user_info(self, access_token):
        # mapping attribute names to keys in dict_user
        attr_mappings = {
            "sub": "sub",
            "name": "name",
            "preferred_username": "preferred_username",
            "email": "email",
            "email_verified": "email_verified",
        }

        def set_attr_value(attr):
            # Use a dictionary to map attribute name to function that sets value in dict_user
            dict_user[attr_mappings[attr["Name"]]] = attr["Value"]

        try:
            client = boto3.client("cognito-idp")
            response = client.get_user(AccessToken=access_token)

            dict_user = {}
            attrs = response["UserAttributes"]
            for attr in attrs:
                if attr["Name"] in attr_mappings:
                    set_attr_value(attr)

            current_app.logger.debug(
                json.dumps(dict_user, sort_keys=True, indent=2, default=str)
            )
            return dict_user
        except Exception as e:
            current_app.logger.debug(f"Error: {e}")
            return extract_current_user(request.headers)


def token_service_factory(user_pool_id, user_pool_client_id, region):
    return CognitoJwtToken(user_pool_id, user_pool_client_id, region)


def authentication_required(view=None, on_error=None):
    if view is None:
        return partial(authentication_required, on_error=on_error)

    @wraps(view)
    def decorated(*args, **kwargs):
        access_token = extract_access_token(request.headers)
        try:
            user_pool_id = os.getenv("AWS_COGNITO_USER_POOL_ID")
            user_pool_client_id = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID")
            region = os.getenv("AWS_DEFAULT_REGION")
            token_service = token_service_factory(
                user_pool_id, user_pool_client_id, region
            )
            claims = token_service.verify(access_token)
            g.cognito_claims = claims
            print(f"claims: ===========> {claims}")

            # current user
            current_user = token_service.get_user_info(access_token)
            print(f"current user:  =========> {current_user}")
            if current_user:
                g.current_user = current_user
        except TokenVerifyError as e:
            # unauthenticated request
            _ = request.data
            current_app.logger.debug(e)
            if on_error:
                return on_error(e)
            abort(make_response(jsonify(message=str(e)), 401))

        return view(*args, **kwargs)

    return decorated


def jwt_required(f=None, on_error=None):
    if f is None:
        return partial(jwt_required, on_error=on_error)

    @wraps(f)
    def decorated_function(*args, **kwargs):
        cognito_jwt_token = CognitoJwtToken(
            user_pool_id=os.getenv("AWS_COGNITO_USER_POOL_ID"),
            user_pool_client_id=os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
            region=os.getenv("AWS_DEFAULT_REGION"),
        )
        access_token = extract_access_token(request.headers)
        try:
            claims = cognito_jwt_token.verify(access_token)
            # is this a bad idea using a global?
            g.cognito_user_id = claims[
                "sub"
            ]  # storing the user_id in the global g object
        except TokenVerifyError as e:
            # unauthenticated request
            app.logger.debug(e)
            if on_error:
                on_error(e)
            return {}, 401
        return f(*args, **kwargs)

    return decorated_function
