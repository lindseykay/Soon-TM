steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE reminders (
            id SERIAL PRIMARY KEY NOT NULL,
            user_id INT,
            email_target VARCHAR(64) NOT NULL,
            reminder_date DATE NOT NULL,
            message_id INT NOT NULL,
            sent boolean DEFAULT FALSE NOT NULL,
            sent_on DATE,
            recurring BOOLEAN DEFAULT FALSE NOT NULL,
            created_on DATE DEFAULT NOW() NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE reminders;
        """
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE messages (
            id SERIAL PRIMARY KEY NOT NULL,
            template_id INT,
            content text NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE messages;
        """
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE reminders_recipients_mapping_table (
            reminder_id INT NOT NULL,
            recipient_id INT NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE reminders_recipients_mapping_table;
        """
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE recipients (
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(50) NOT NULL,
            phone VARCHAR(20),
            email VARCHAR(64),
            user_id INT
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE recipients;
        """
    ]
]
