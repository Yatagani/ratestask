import psycopg2

from os import environ

def execute_query(query):
    connection = None
    try:
        connection = psycopg2.connect(
            host=environ.get("DATABASE_HOST"),
            database="postgres",
            user="postgres",
            password=environ.get("POSTGRES_PASSWORD"),
            port=5432)

        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection is not None:
            connection.close()


def extract_codes(location):
    query_codes = execute_query(
        f"""
        SELECT ports.code
        FROM ports
        JOIN regions ON regions.slug = ports.parent_slug
        WHERE regions.parent_slug = '{location}' OR ports.code = '{location}' OR ports.parent_slug = '{location}'
        """)

    codes = list(map(lambda x: x[0], query_codes))

    str_codes = ','.join(f"'{code}'" for code in codes)

    return str_codes
