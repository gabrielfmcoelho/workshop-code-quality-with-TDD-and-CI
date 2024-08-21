from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .src.settings import AppSettings
from .src.routes import users_router, database_router


app_s = AppSettings()

app = FastAPI(
    title=app_s.TITLE,
    version=app_s.VERSION,
    description=app_s.DESCRIPTION,
    contact={"name": app_s.CONTACT_NAME, "email": app_s.CONTACT_EMAIL},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_s.allowed_origins,
    allow_credentials=app_s.allowed_credentials,
    allow_methods=app_s.allowed_methods,
    allow_headers=app_s.allowed_headers,
)

app.include_router(database_router)
app.include_router(users_router)
