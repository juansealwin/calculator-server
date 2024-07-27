# Calculator server

This is the backend for the calculator app.

## Setup

1. Clone the repository:
```
sh
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

