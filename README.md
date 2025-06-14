# Payment Gateway API

A RESTful API for processing payments, designed for small businesses. This API provides endpoints for initiating and tracking payments without requiring user authentication.

## Features

- RESTful API with versioning
- Payment processing endpoints
- No authentication required
- Automated testing
- CI/CD pipeline with GitHub Actions

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd payment-gateway
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

### 1. Initiate a Payment
- **URL**: `/api/v1/payments/`
- **Method**: `POST`
- **Request Body**:
```json
{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "amount": 50.00
}
```

### 2. Retrieve Payment Status
- **URL**: `/api/v1/payments/{id}/`
- **Method**: `GET`
- **Response**:
```json
{
    "payment": {
        "id": "PAY-123",
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "amount": 50.00,
        "status": "completed"
    },
    "status": "success",
    "message": "Payment details retrieved successfully."
}
```

## Running Tests

To run the test suite:
```bash
python manage.py test
```

## CI/CD Pipeline

The project includes a GitHub Actions workflow that:
1. Runs on push to main branch and pull requests
2. Sets up Python environment
3. Installs dependencies
4. Runs tests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 