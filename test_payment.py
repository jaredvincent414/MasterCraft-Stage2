import requests
import json

def create_payment():
    url = 'http://localhost:8000/api/v1/payments/'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        'customer_name': 'Test User',
        'customer_email': 'test@example.com',
        'amount': '10.00'
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f'Status Code: {response.status_code}')
    print('Response:')
    print(json.dumps(response.json(), indent=2))

if __name__ == '__main__':
    create_payment() 