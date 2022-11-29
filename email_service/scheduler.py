import time
import schedule
from typing import Optional, Union, List
from pools import pool
from datetime import date

def reminder_compiler():
    try:
        with pool.connection() as conn:
            with conn.cursor() as db:
                result = db.execute(
                    """
                    SELECT *
                    FROM reminders
                    WHERE sent = false
                    AND reminder_date = %s
                    """,
                    [date.today()]
                )
                query = result.fetchall()
                dict = {}
                for record in query:
                    if record[2] not in dict:
                        dict[record[2]] = [{
                            "recipients": get_recipients(record[0]),
                            "message": get_message_content(record[4])
                        }]

                    else:
                        dict[record[2]].append(
                            {
                                "recipients": get_recipients(record[0]),
                                "message": get_message_content(record[4])
                            }
                        )
                print("THIS IS THE NEW ONE DICT:::", dict, flush=True)
                return dict
    except Exception:
        return print("No good")

#     ----helper functions----

def get_recipients(reminder_id):
    try:
        with pool.connection() as conn:
            with conn.cursor() as db:
                result = db.execute(
                    """
                    SELECT recipient_id
                    FROM reminders_recipients_mapping_table
                    WHERE reminder_id = %s
                    """,
                    [reminder_id]
                )
                recipient_id_query = result.fetchall()
                recipient_ids = []
                for recipient in recipient_id_query:
                    recipient_ids.append(recipient[0])
                recipient_list = []
                for id in recipient_ids:
                    id_query = db.execute(
                        """
                        SELECT name
                            , phone
                            , email
                        FROM recipients
                        WHERE id = %s
                        """,
                        [id]
                    )
                    query = id_query.fetchall()
                    recipient_list.append({
                        "name": query[0][0],
                        "phone": query[0][1],
                        "email": query[0][2]
                    })
                return recipient_list
    except Exception:
        return print("No recipients")

def get_message_content(message_id):
    try:
        with pool.connection() as conn:
            with conn.cursor() as db:
                result = db.execute(
                    """
                    SELECT content
                    FROM messages
                    WHERE id = %s
                    """,
                    [message_id]
                )
                query = result.fetchone()
                return str(query[0])
    except Exception:
        return print("No message")

#   ----SCHEDULER----

def compiler_scheduler():
    schedule.every().day.at("08:00:00").do(reminder_compiler)

    while True:
        schedule.run_pending()