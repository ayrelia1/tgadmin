from fastapi import FastAPI, HTTPException, Request, Cookie, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from exc import NotAuthenticatedException
from routers import routers
from config import app
from db.models import create_tables
from db.db import engine


@app.exception_handler(NotAuthenticatedException)
async def not_authenticated_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url="/login", status_code=303)


for router in routers:
    app.include_router(router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)