from fastapi import FastAPI
from src.routers import auth, users, groups, messages

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(messages.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)