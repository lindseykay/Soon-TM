steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE reminders (
            id serial primary key not null,
            user_id int,
            email_target varchar(64) not null,
            reminder_date date not null,
            message_id int not null,
            sent boolean default false not null,
            sent_on date,
            recurring boolean default false not null,
            created_on date default now() not null
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
            id serial primary key not null,
            template_id int,
            content text not null
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
            reminder_id int not null,
            recipient_id int not null
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE recipients_list;
        """
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE recipients (
            id serial primary key not null,
            name varchar(50) not null,
            phone varchar(20),
            email varchar(64)
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE recipients;
        """
    ]
]
