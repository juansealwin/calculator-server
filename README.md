# Calculator server

This is the backend for the calculator app.

## Setup

1. Clone the repository:

```
git clone https://github.com/your-username/calculator-backend.git
cd calculator-backend
```

2. Create and activate a virtual environment:

```
python -m venv env
source env/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Start the application:

```
uvicorn app.main:app --reload
```

## Environment Variables

This app uses env variables (create a `.env` file in the root of the project):

DATABASE_URL=sqlite:///./test.db
SK_JWT='secretkey'

- `DATABASE_URL`: The URL for the db connection. Default `sqlite:///./test.db`.
- `SK_JWT`: For JWT encoding.


## API Documentation

- **Base URL:** `/api/v1`

### Authentication

#### Register

- **Endpoint:** `/api/v1/register`
- **Method:** `POST`
- **Summary:** Register a new user
- **Request Body:**
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
- **Responses:**
    - **200 OK:** User created successfully
    - **422 Unprocessable Entity:** Validation error

#### Login

- **Endpoint:** `/api/v1/login`
- **Method:** `POST`
- **Summary:** Login a user and obtain a token
- **Request Body:**
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
- **Responses:**
    - **200 OK:** Token obtained successfully
    - **422 Unprocessable Entity:** Validation error

### Operations

#### Create Operation

- **Endpoint:** `/api/v1/operations`
- **Method:** `POST`
- **Summary:** Create a new operation
- **Request Body:**
    ```json
    {
      "type": "string",
      "amount1": "number or null",
      "amount2": "number or null"
    }
    ```
- **Responses:**
    - **200 OK:** Operation created successfully
    - **422 Unprocessable Entity:** Validation error
    - **402 Insufficient balance** 
- **Security:** OAuth2

### Records

#### Read Records

- **Endpoint:** `/api/v1/records`
- **Method:** `GET`
- **Summary:** Retrieve a list of records with optional filtering, pagination, and sorting.
- **Parameters:**
    - `skip`: Integer (default: 0)
    - `limit`: Integer (default: 10)
    - `search`: String or null
    - `sort_by`: String or null
    - `sort_order`: String (default: "asc")
- **Responses:**
    - **200 OK:** List of records
    - **422 Unprocessable Entity:** Validation error
- **Security:** OAuth2

#### Delete Record

- **Endpoint:** `/api/v1/records/{record_id}`
- **Method:** `DELETE`
- **Summary:** Delete a specific record
- **Parameters:**
    - `record_id`: Integer (path parameter)
- **Responses:**
    - **200 OK:** Record deleted successfully
    - **422 Unprocessable Entity:** Validation error
- **Security:** OAuth2

### Balances

#### Read Balance

- **Endpoint:** `/api/v1/balances/{user_id}`
- **Method:** `GET`
- **Summary:** Retrieve the balance of a specific user
- **Parameters:**
    - `user_id`: Integer (path parameter)
- **Responses:**
    - **200 OK:** User's balance
    - **422 Unprocessable Entity:** Validation error
- **Security:** OAuth2

#### Update Balance

* **This endpoint is only for testing purposes**

- **Endpoint:** `/api/v1/balances/{user_id}`
- **Method:** `PUT`
- **Summary:** Update the balance of a specific user (for testing propouses)
- **Parameters:**
    - `user_id`: Integer (path parameter)
- **Request Body:**
    ```json
    {
      "amount": "number"
    }
    ```
- **Responses:**
    - **200 OK:** Balance updated successfully
    - **422 Unprocessable Entity:** Validation error
- **Security:** OAuth2


See the API documentation detial in Swagger UI, available at `/docs` after starting the server.