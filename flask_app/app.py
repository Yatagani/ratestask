from flask import Flask, request, jsonify

from helpers import extract_codes
from queries import get_average_prices
from validators import validate_rates_query_params

app = Flask(__name__)

@app.route('/rates', methods=['GET'], strict_slashes=False)
def rates():
    args = request.args.to_dict()
    
    errors = validate_rates_query_params(args)

    if errors is not None:
        return errors, 400

    orig_codes = extract_codes(args['origin'])
    dest_codes = extract_codes(args['destination'])

    result = get_average_prices(args['date_from'], args['date_to'], orig_codes, dest_codes)

    return jsonify(result)

if __name__ == '__main__':
  app.run()
