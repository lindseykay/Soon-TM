from queries.pools import conn
from typing import List

class ReminderRecipientMappingRepository:
    def create(self, reminder_id: int, recipient_id: int):
        try:
            # with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        INSERT INTO reminders_recipients_mapping_table(
                            reminder_id
                            , recipient_id
                        )
                        VALUES (%s, %s);
                        """,
                        [
                            reminder_id,
                            recipient_id
                        ]
                    )
        except Exception:
            return {"message": "create reminder recipient record failed"}

    def delete(self, reminder_id: int):
        try:
            # with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        DELETE FROM reminders_recipients_mapping_table
                        WHERE reminder_id = %s
                        """,
                        [
                            reminder_id
                        ]
                    )
        except Exception:
            return {"message": "delete reminder recipients record failed"}

    def update(self, reminder_id: int, recipients: List[int]) -> bool:
        try:
            # with pool.connection() as conn:
                with conn.cursor() as db:
                    self.delete(reminder_id)
                    db.execute(
                        """
                        INSERT INTO reminders_recipients_mapping_table(
                            reminder_id
                            , recipient_id
                        )
                        VALUES (%s, UNNEST(CAST(%s AS INT [])))
                        """,
                        [
                            reminder_id,
                            recipients
                        ]
                    )
                    return True
        except Exception:
            return False
