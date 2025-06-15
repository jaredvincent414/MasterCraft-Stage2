
# Payment Gateway API for Small Businesses

This **RESTful API** is designed to simplify payment processing for small businesses. It provides secure and straightforward endpoints for initiating and tracking payments, all without user authentication. Get up and running quickly to start accepting payments\!

## ✨ Features

  * **RESTful API with Versioning**: This is a clean and organized API structure that's easy to understand and use, with versioning for future scalability.
  * **Payment Processing Endpoints**: Dedicated endpoints to securely handle payment initiation and status retrieval.
  * **No Authentication Required**: Streamlined access for quick integration and use.
  * **Automated Testing**: A Comprehensive test suite ensures reliability and stability.
  * **CI/CD Pipeline with GitHub Actions**: Automated deployment and testing workflows for consistent updates and quality.

-----

## Live Demo

This API is currently deployed and live on Render\! You can access it here:

**[https://mastercraft-stage2-3.onrender.com](https://mastercraft-stage2-3.onrender.com)**

-----

## Requirements

  * **Python 3.8 or higher**
  * **pip** (Python package manager)
  * **Virtual environment** (highly recommended for dependency management)

-----

## Installation

Follow these simple steps to get the API running locally:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/jaredvincent414/MasterCraft-Stage2
    cd payment-gateway
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Start the development server:**

    ```bash
    python manage.py runserver
    ```

-----

## API Endpoints

Here's how you can interact with the API:

### 1\. Initiate a Payment

  * **URL**: `/api/v1/payments/`

  * **Method**: `POST`

  * **Request Body Example**:

    ```json
    {
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "amount": 50.00
    }
    ```

### 2\. Retrieve Payment Status

  * **URL**: `/api/v1/payments/{id}/` (Replace `{id}` with the actual payment ID)

  * **Method**: `GET`

  * **Successful Response Example**:

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

-----

## Running Tests

Ensure everything is working as expected by running the test suite:

```bash
python manage.py test
```

-----

## CI/CD Pipeline

This project leverages **GitHub Actions** for an automated CI/CD pipeline. This workflow automatically:

1.  Runs on pushes to the `main` branch and on pull requests.
2.  Sets up the Python environment.
3.  Installs all necessary dependencies.
4.  Executes the test suite to maintain code quality.

-----

