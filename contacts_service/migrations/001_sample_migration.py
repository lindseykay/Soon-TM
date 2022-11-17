steps = [
    [
        # "Up" SQL statement
        """
        create table contacts (
            id serial primary key not null,
            recipient_id int not null,
            special_days_id int,
            notes text
        );
        """,
        # "Down" SQL statement
        """
        drop table contacts;
        """
    ],
    [
        # "Up" SQL statement
        """
        create table special_days (
            id serial primary key not null,
            name varchar(100) not null,
            date date not null
        );
        """,
        # "Down" SQL statement
        """
        drop table special_days;
        """
    ],
]
