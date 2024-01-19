from typing import Annotated

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.features.country.router import router as countryRouter
from src.features.earthquake.router import router as earthQuakeRouter

app = FastAPI()

origins = [
    "http://localhost:2402",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(countryRouter, prefix='/countries', tags=['country'])
app.include_router(earthQuakeRouter, prefix='/earthquakes', tags=['earthquake'])