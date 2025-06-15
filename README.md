
#  Payment Gateway API for Small Businesses

A simplified **RESTful API** designed to simplify payment processing for small businesses using paypal. It enables seamless payment initiation and status tracking—**no user authentication required**.

---

##  Features

* **RESTful API with Versioning**
* **Payment Endpoints**
* **No Authentication** 
* **Automated Testing** 
* **CI/CD with GitHub Actions**

---

## Live Demo

The API is live and deployed on Render:

[https://mastercraft-stage2-3.onrender.com](https://mastercraft-stage2-3.onrender.com)

---

## Requirements

* Python 3.8 or higher
* pip (Python package manager)
* Virtual environment (recommended)

---

## Setup & Installation

Follow these steps to run the API locally:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/jaredvincent414/MasterCraft-Stage2
   cd payment-gateway
   ```

2. **Create & Activate Virtual Environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

---

## 📡 API Endpoints

### 1. Initiate Payment

* **Endpoint**: `POST /api/v1/payments/`
* **Request Body**:

  ```json
  {
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "amount": 50.00
  }
  ```

---

### 2. Retrieve Payment Status

* **Endpoint**: `GET /api/v1/payments/{id}/`
* **Path Parameter**: `{id}` = Payment ID
* **Example Response**:

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

---

## Running Tests

To verify the application and ensure everything works:

```bash
python manage.py test
```

---

## CI/CD Pipeline

Powered by **GitHub Actions**, the CI/CD workflow:

1. Triggers on `push` to `main` or PRs.
2. Sets up the Python environment.
3. Installs all dependencies.
4. Runs the full test suite for continuous validation.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

