from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from src.features.country.router import router as countryRouter
from src.features.earthquake.router import router as earthQuakeRouter

app = FastAPI()

app.include_router(countryRouter, prefix='/countries', tags=['country'])
app.include_router(earthQuakeRouter, prefix='/earthquakes', tags=['earthquake'])