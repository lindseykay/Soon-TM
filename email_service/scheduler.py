import time
import schedule
from pools import pool
from datetime import date
from emailer import formatter, send_emails

def reminder_compiler():
    try:
        with pool.connection() as conn:
            with conn.cursor() as db:
                result = db.execute(
                    """
                    SELECT r.id AS reminder_id
                        , r.user_id
                        , r.email_target
                        , m.content
                        , STRING_AGG(re.name || ' || ' || re.phone || ' || ' || re.email, ',') AS recipients
                    FROM reminders AS r
                    LEFT JOIN messages AS m ON r.message_id = m.id
                    LEFT JOIN reminders_recipients_mapping_table AS rrmt ON rrmt.reminder_id = r.id
                    LEFT JOIN recipients AS re ON rrmt.recipient_id = re.id
                    WHERE r.sent = false
                    AND r.reminder_date = %s
                    GROUP BY 1, 2, 3, 4
                    """,
                    [date.today()]
                )
                query = result.fetchall()
                dict = {}
                for record in query:
                    recipients = record[4].split(',')
                    if record[2] not in dict:
                        dict[record[2]] = [{
                            "recipients": [recipient for recipient in recipients],
                            "message": record[3]
                        }]
                    else:
                        dict[record[2]].append({
                            "recipients": [recipient for recipient in recipients],
                            "message": record[3]
                        })
                return dict
    except Exception:
        return print("BAAAD", flush=True)

def job():
    x = reminder_compiler()
    try:
        y = formatter(x)
        send_emails(y)
    except Exception:
        print("You have no reminders or crashed")

#   ----SCHEDULER----

def compiler_scheduler():
    schedule.every().day.at("14:00:00").do(job)


    while True:
        schedule.run_pending()
