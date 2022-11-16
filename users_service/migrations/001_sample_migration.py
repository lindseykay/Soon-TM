steps = [
    [
        # "Up" SQL statement
        """
        create table users (
            id serial primary key not null,
            username varchar(48) unique not null,
            password varchar(48) not null,
            email varchar(64) unique not null,
            name varchar(64) not null
        );
        """,
        # "Down" SQL statement
        """
        drop table users;
        """
    ],
]
