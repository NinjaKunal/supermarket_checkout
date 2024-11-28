# Supermarket Checkout System

A FastAPI-based application for managing a supermarket's checkout process.

## Run Locally Without Docker

1. Clone the repository:
    ```bash
    git clone https://github.com/NinjaKunal/supermarket_checkout.git
    cd supermarket_checkout
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ```

4. Access the API documentation at:
    ```
    http://127.0.0.1:8000/docs
    ```

## Run with Docker

1. Build the Docker image:
    ```bash
    docker build -t supermarket-checkout .
    ```

2. Run the Docker container:
    ```bash
    docker run -p 8000:8000 supermarket-checkout
    ```

3. Access the API documentation at:
    ```
    http://127.0.0.1:8000/docs
    ```

## Testing the Application
1. Run the tests:
    ```bash
    pytest
    ```

2. Ensure all tests pass successfully.