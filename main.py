from fastapi import FastAPI
from src.routers import auth, users, groups, messages

"""
Group Chat API

A FastAPI-based Group Chat API that allows users to create accounts, join groups, send messages, and like messages within groups.

Routers:
- auth: Authentication routes for user login and token generation.
- users: User-related routes for creating and updating user accounts.
- groups: Group-related routes for creating, deleting, listing groups, and adding members to groups.
- messages: Message-related routes for sending messages to groups and liking messages.

Usage:
- Run the API server using `uvicorn main:app --reload`.
- Access the API documentation at `http://localhost:8000/docs` or `http://localhost:8000/redoc`.
"""
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
