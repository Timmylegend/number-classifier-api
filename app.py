from flask import Flask, request, jsonify
import requests
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 1:
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)
    return sum_factors == n

def is_armstrong(n):
    num_str = str(n)
    power = len(num_str)
    total = sum(int(digit) ** power for digit in num_str)
    return total == n

def get_digit_sum(n):
    return sum(int(digit) for digit in str(abs(n)))

def get_properties(n):
    properties = []
    
    # Check if number is Armstrong
    if is_armstrong(n):
        properties.append("armstrong")
    
    # Check if odd or even
    properties.append("odd" if n % 2 else "even")
    
    return properties

def get_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        if response.status_code == 200:
            return response.text
        else:
            # Fallback fun fact if API fails
            if is_armstrong(n):
                digits = str(n)
                calc = " + ".join([f"{d}^{len(digits)}" for d in digits])
                return f"{n} is an Armstrong number because {calc} = {n}"
            return f"The number {n} is {'even' if n % 2 == 0 else 'odd'}"
    except:
        # Fallback fun fact if API is unreachable
        return f"The number {n} is {'even' if n % 2 == 0 else 'odd'}"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        number = request.args.get('number', type=int)
        if number is None:
            return jsonify({
                "number": request.args.get('number', ''),
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

    except ValueError:
        return jsonify({
            "number": request.args.get('number', ''),
            "error": True
        }), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=5000)
