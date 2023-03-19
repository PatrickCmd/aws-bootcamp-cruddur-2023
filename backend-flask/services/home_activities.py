from datetime import datetime, timedelta, timezone

from opentelemetry import trace

from utils.db import db

tracer = trace.get_tracer(__name__)


class HomeActivities:
    def run(logger, cognito_user_id=None):
        logger.info("HomeActivities Cloudwatch Log! from  /api/activities/home")
        with tracer.start_as_current_span("home-activities-mock-data"):
            span = trace.get_current_span()
            now = datetime.now(timezone.utc).astimezone()
            span.set_attribute("app.now", now.isoformat())

            sql = db.template("activities", "home")
            results = db.query_array_json(sql)
            return results
