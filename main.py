from fastapi import FastAPI
from src.routers import auth, users, groups, messages

app = FastAPI(title="Group Chat API",
    description="A FastAPI-based Group Chat API that allows users to create accounts, join groups, send messages, and like messages within groups.",
    version="1.0.0",)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(messages.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
