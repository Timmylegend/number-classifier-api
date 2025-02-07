# Number Classification API

A RESTful API that provides mathematical properties and fun facts about numbers. This API analyzes numbers for various properties including primality, perfect numbers, Armstrong numbers, and provides interesting mathematical facts.

## Features

- Number classification and analysis
- Cross-Origin Resource Sharing (CORS) enabled
- JSON response format
- Error handling for invalid inputs
- Integration with Numbers API for fun facts
- Fallback mechanisms for external API failures

## API Specification

### Endpoint

```
GET /api/classify-number?number={integer}
```

### Success Response (200 OK)

```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

### Error Response (400 Bad Request)

```json
{
    "number": "invalid_input",
    "error": true
}
```

## Properties Explained

- `is_prime`: True if the number is only divisible by 1 and itself
- `is_perfect`: True if the sum of its proper divisors equals the number
- `properties`: Array containing "armstrong" and/or "odd"/"even"
- `digit_sum`: Sum of all digits in the number
- `fun_fact`: Interesting mathematical fact about the number

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/number-classifier-api.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Requirements

- Python 3.7+
- Flask
- Flask-CORS
- Requests

## Deployment

The API can be deployed to any platform that supports Python applications. Some recommended platforms:
- Heroku
- PythonAnywhere
- Google Cloud Platform
- AWS Elastic Beanstalk

## Testing

Test the API using curl or any HTTP client:

```bash
curl "http://your-domain.com/api/classify-number?number=371"
```

## Error Handling

The API handles various error cases:
- Invalid input types
- Missing parameters
- External API failures
- Server errors

## Performance

- Average response time: <500ms
- Handles concurrent requests efficiently
- Includes fallback mechanisms for external API failures

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
