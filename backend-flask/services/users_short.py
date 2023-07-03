from utils.db import db


class UsersShort:
    def run(handle):
        """Return a user object"""
        sql = db.template("users", "short")
        results = db.query_object_json(sql, {"handle": handle})
        return results
