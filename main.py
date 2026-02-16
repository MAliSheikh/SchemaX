from fastapi import FastAPI
from api import auth, users

app = FastAPI(title="FastAPI Production Boilerplate")

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
