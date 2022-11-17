steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE templates (
            id SERIAL PRIMARY KEY NOT NULL,
            public boolean NOT NULL,
            theme_id INT,
            user_id INT,
            name VARCHAR(100) NOT NULL,
            content TEXT NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE templates;
        """
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE themes (
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(50) NOT NULL,
            picture_url VARCHAR(255) NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE themes;
        """
    ]
]
