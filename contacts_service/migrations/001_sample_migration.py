steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE contacts (
            id SERIAL PRIMARY KEY NOT NULL,
            recipient_id INT NOT NULL,
            special_days_id INT,
            notes TEXT
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE contacts;
        """
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE special_days (
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(100) NOT NULL,
            date DATE NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE special_days;
        """
    ],
]
