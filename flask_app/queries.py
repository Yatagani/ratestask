from helpers import execute_query

def get_average_prices(date_from, date_to, origin, destination):
    query_result = execute_query(
        f"""
            SELECT day,
                CASE
                    WHEN COUNT(price) >= 3 THEN CAST(ROUND(AVG(price)) AS integer)
                    ELSE NULL
                END AS average_price
            FROM prices
            WHERE orig_code in ({origin})
                AND dest_code in ({destination})
                AND day BETWEEN '{date_from}' AND '{date_to}' 
            GROUP BY day
            ORDER BY day
        """
    )

    response = [{ 'day': str(day), 'average_price': avg_price } for day, avg_price in query_result]

    return response