from queries.pools import pool

class ReminderRecipientMappingRepository:
    def create(self, reminder_id: int, recipient_id: int):
        try:
            with pool.connection() as conn:
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