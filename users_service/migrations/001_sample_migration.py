steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY NOT NULL,
            username VARCHAR(48) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(64) UNIQUE NOT NULL,
            name VARCHAR(64) NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE users;
        """,
    ],
]
