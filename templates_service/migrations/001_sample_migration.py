steps = [
    [
        # "Up" SQL statement
        """
        create table templates (
            id serial primary key not null,
            public boolean not null,
            theme_id int,
            user_id int,
            name varchar(100) not null,
            content text not null
        );
        """,
        # "Down" SQL statement
        """
        drop table templates;
        """
    ],
    [
        # "Up" SQL statement
        """
        create table themes (
            id serial primary key not null,
            name varchar(50) not null,
            picture_url varchar(255) not null
        );
        """,
        # "Down" SQL statement
        """
        drop table themes;
        """
    ]
]
