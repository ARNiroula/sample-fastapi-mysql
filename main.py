from fastapi import FastAPI

from lifespan import lifespan
from controllers import users, posts


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def health_check():
    return "Server is Running"

app.include_router(users.router)
app.include_router(posts.router)
