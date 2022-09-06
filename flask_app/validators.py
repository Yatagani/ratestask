from jsonschema import validate, ValidationError, FormatChecker
from helpers import execute_query

def validate_rates_query_params(params):
    schema = {
        "type" : "object",
        "properties" : {
            "date_from" : {"type" : "string", "format": "date"},
            "date_to" : {"type" : "string", "format": "date"},
            "origin" : {"type" : "string"},
            "destination" : {"type" : "string"},
            },
        "required" : ["date_from", "date_to", "origin", "destination"]
    }

    try:
        # validate() returns None if validation was successful, otherwise raises an error
        validator = validate(instance=params, schema=schema, format_checker=FormatChecker()) 

        locations = [
            params['origin'], 
            params['destination']
        ]

        for location in locations:
            target = execute_query(f"SELECT code FROM ports WHERE '{location}' IN (code, parent_slug)")

            if not target:
                return { "error": f"{location} does not exist in the database" }

        if params['date_from'] > params['date_to']:
            return { "error": "Invalid date period"}

        return validator
    except ValidationError as error:
        return { 'error' : error.message }