from fastapi import FastAPI
from .routers import auth, operations, balance
from .database import init_db

app = FastAPI()

init_db()

@app.get("/")
def read_root():
    return {"message": "Calculator App"}

app.include_router(auth.router)
app.include_router(operations.router)
app.include_router(balance.router)
