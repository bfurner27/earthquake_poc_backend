from typing import Annotated
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from src.features.shared.dependencies import get_db

from .api_model import CountryCreateInput, CountryValidateOutput, CountryValidateOutputData
from ..country import db_repo as db
from .internal_model import Boundaries, CreateCountryInternal

router = APIRouter()

@router.get('')
def read_countries():
    pass

@router.post('')
def create_countries(body: CountryCreateInput, dbSession: Session = Depends(get_db)) -> CountryValidateOutputData:
    create_db_entries: CreateCountryInternal = [ CreateCountryInternal(
        c.name, 
        Boundaries(c.coordinates, c.shapeType),
        c.requestId
    ) for c in body.data]
    created = db.create_countries(dbSession, create_db_entries)

    results: list[CountryValidateOutput] = [ CountryValidateOutput(id = c.id, name = c.name, requestId = c.requestId ) for c in created ]

    return CountryValidateOutputData(
        data = results,
        errors = [],
    )

@router.get('/{id}')
def read_country(id: int):
    pass

@router.put('/{id}')
def update_country(id: int):
    pass

@router.delete('/{id}')
def delete_country(id: int):
    pass