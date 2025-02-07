from flask import Flask, request, jsonify
import requests
import math
from flask_cors import CORS
import concurrent.futures
from functools import lru_cache

app = Flask(__name__)
CORS(app)

# Cache results to improve performance
@lru_cache(maxsize=1000)
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

@lru_cache(maxsize=1000)
def is_perfect(n):
    if n < 1:
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)
    return sum_factors == n

@lru_cache(maxsize=1000)
def is_armstrong(n):
    num_str = str(n)
    power = len(num_str)
    total = sum(int(digit) ** power for digit in num_str)
    return total == n

def get_digit_sum(n):
    return sum(int(digit) for digit in str(abs(n)))

def get_properties(n):
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    properties.append("odd" if n % 2 else "even")
    return properties

# Timeout for external API requests
TIMEOUT = 1.0  # 1 second timeout

def get_fun_fact(n):
    try:
        response = requests.get(
            f"http://numbersapi.com/{n}/math",
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return response.text
        raise Exception("API error")
    except:
        # Immediate fallback without waiting
        if is_armstrong(n):
            digits = str(n)
            calc = " + ".join([f"{d}^{len(digits)}" for d in digits])
            return f"{n} is an Armstrong number because {calc} = {n}"
        return f"The number {n} is {'even' if n % 2 == 0 else 'odd'}"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        # Get number parameter and validate
        number = request.args.get('number', type=int)
        if number is None:
            return jsonify({
                "number": request.args.get('number', ''),
                "error": True
            }), 400

        # Calculate all properties concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            prime_future = executor.submit(is_prime, number)
            perfect_future = executor.submit(is_perfect, number)
            properties_future = executor.submit(get_properties, number)
            digit_sum_future = executor.submit(get_digit_sum, number)
            fun_fact_future = executor.submit(get_fun_fact, number)

            result = {
                "number": number,
                "is_prime": prime_future.result(),
                "is_perfect": perfect_future.result(),
                "properties": properties_future.result(),
                "digit_sum": digit_sum_future.result(),
                "fun_fact": fun_fact_future.result()
            }

        # Ensure Content-Type is application/json
        return jsonify(result), 200

    except ValueError:
        return jsonify({
            "number": request.args.get('number', ''),
            "error": True
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)