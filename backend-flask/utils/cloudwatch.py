from time import strftime

from flask import request


def init_cloudwatch(response, LOGGER):
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
