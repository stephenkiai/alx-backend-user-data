#!/usr/bin/env python3
"""
filtered_logger module for obfuscating log messages
"""

import re
import logging
import os
import mysql.connector
from datetime import datetime

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


# 0. Regex-ing task
def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate specified fields in the log message.

    Returns:
        str: Log message with specified fields obfuscated.
    """
    for field in fields:
        pattern = re.compile(r'(?<={}=)[^{}]+'.format(field, separator))
        message = pattern.sub(redaction, message)
    return message


# 1. Log formatter task
class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """
        Initializes the RedactingFormatter instance.
        Args:
            fields (list): List of strings representing fields to redact.

        """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record and obfuscates sensitive information.
        """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


# 2. Create logger task
def get_logger():
    """Creates and configures a logging.Logger object.

    Returns:
        logging.Logger: The configured logger.

    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


# 3. Connect to secure database task
def get_db():
    """Connect to the database and return a MySQLConnection object."""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return db


# 4. Read and filter data task
def main():
    """
    Retrieve all rows from the users table and display in a filtered format.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('[HOLBERTON] user_data INFO %(asctime)-15s: %(message)s', '%Y-%m-%d %H:%M:%S')
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    filtered_fields = ["name", "email", "phone", "ssn", "password"]

    for row in cursor:
        filtered_data = '; '.join(f"{field}={row[field] if field not in filtered_fields else '***'}" for field in row)
        logger.info(filtered_data)

    cursor.close()
    db.close()

"""Only 'main' function should run when the module is executed."""
if __name__ == "__main__":
    main()