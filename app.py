from flask import Flask, request, jsonify
import requests
import math
from flask_cors import CORS
from functools import lru_cache

app = Flask(__name__)
CORS(app)

@lru_cache(maxsize=1000)
def is_prime(n):
    # Handle negative numbers and non-integers
    n = abs(int(n))
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

@lru_cache(maxsize=1000)
def is_perfect(n):
    # Handle negative numbers and non-integers
    n = abs(int(n))
    if n < 1:
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)
    return sum_factors == n

@lru_cache(maxsize=1000)
def is_armstrong(n):
    # Handle negative numbers and non-integers
    n = abs(int(n))
    num_str = str(n)
    power = len(num_str)
    total = sum(int(digit) ** power for digit in num_str)
    return total == n

def get_digit_sum(n):
    # Handle negative numbers and non-integers
    return sum(int(digit) for digit in str(abs(int(n))))

def get_properties(n):
    # Handle negative numbers and non-integers
    n = int(n)
    properties = []
    if is_armstrong(abs(n)):
        properties.append("armstrong")
    properties.append("odd" if n % 2 else "even")
    return properties

TIMEOUT = 1.0

def get_fun_fact(n):
    try:
        response = requests.get(
            f"http://numbersapi.com/{int(n)}/math",
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return response.text
        raise Exception("API error")
    except:
        # Immediate fallback
        n = int(n)
        if is_armstrong(abs(n)):
            digits = str(abs(n))
            calc = " + ".join([f"{d}^{len(digits)}" for d in digits])
            return f"{abs(n)} is an Armstrong number because {calc} = {abs(n)}"
        return f"The number {n} is {'even' if n % 2 == 0 else 'odd'}"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        # Get number parameter and convert to float first
        number_str = request.args.get('number', '')
        if not number_str:
            return jsonify({
                "number": number_str,
                "error": True
            }), 400

        try:
            # Try converting to float first to handle decimal points
            number = float(number_str)
            # Convert to int if it's a whole number
            if number.is_integer():
                number = int(number)
        except ValueError:
            return jsonify({
                "number": number_str,
                "error": True
            }), 400

        result = {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": get_properties(number),
            "digit_sum": get_digit_sum(number),
            "fun_fact": get_fun_fact(number)
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "number": request.args.get('number', ''),
            "error": True
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)