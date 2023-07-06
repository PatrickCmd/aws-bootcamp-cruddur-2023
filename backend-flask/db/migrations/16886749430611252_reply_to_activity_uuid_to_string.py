from utils.db import db


class ReplyToActivityUuidToStringMigration:
    def migrate_sql():
        data = """
        -- Could not directly convert integer to uuid so recfactored query to one below after these two statements
        -- ALTER TABLE activities
        -- ALTER COLUMN reply_to_activity_uuid TYPE uuid USING reply_to_activity_uuid::uuid;

        -- Add a new UUID column
        ALTER TABLE activities ADD COLUMN new_reply_to_activity_uuid UUID;
        -- Update the new column with the converted values
        UPDATE activities SET new_reply_to_activity_uuid = uuid_generate_v4()::uuid;
        -- Once you've confirmed the data is correct, you can drop the old column and rename the new column
        ALTER TABLE activities DROP COLUMN "reply_to_activity_uuid";
        ALTER TABLE activities RENAME COLUMN new_reply_to_activity_uuid TO "reply_to_activity_uuid";
        """
        return data

    def rollback_sql():
        data = """
        ALTER TABLE activities
        ALTER COLUMN reply_to_activity_uuid TYPE integer USING (reply_to_activity_uuid::integer);
        """
        return data

    def migrate():
        db.query_commit(ReplyToActivityUuidToStringMigration.migrate_sql(), {})

    def rollback():
        db.query_commit(ReplyToActivityUuidToStringMigration.rollback_sql(), {})


migration = ReplyToActivityUuidToStringMigration
