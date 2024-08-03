from fastapi import FastAPI
from .routers import auth, operations, balance
from .database import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

init_db()

# CORS config
origins = [
    "http://localhost:3000",
    "https://juansealwin.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Calculator App"}

app.include_router(auth.router)
app.include_router(operations.router)
app.include_router(balance.router)
