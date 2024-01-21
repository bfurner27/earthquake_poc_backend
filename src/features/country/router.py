from datetime import datetime, timedelta
import sys
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from src.features.earthquake.internal_model import EarthQuakeInternal
from src.features.shared.db_repo import OrderBy

from src.features.shared.dependencies import get_db

from .api_model import CountryCreateInput, CountryValidateOutput, CountryValidateOutputData, TopCountryEarthquakeCount, TopCountryEarthquakeCountResponse
from ..country import db_repo as db
from ..earthquake import db_repo as earthquakeDb
from .internal_model import Boundaries, CountryInternal, CreateCountryInternal

router = APIRouter()

@router.get('')
def read_countries():
    pass

@router.get('/most-earthquakes')
def most_recent_earthquakes(dbSession: Session = Depends(get_db)) -> TopCountryEarthquakeCountResponse:
    params = earthquakeDb.ReadEarthquakeParams(
        0, 
        20000, 
        orderBy=OrderBy('date'), 
        minDatetime=(datetime.now() - timedelta(days = 365 * 10))
    )

    earthquakes = earthquakeDb.read_earthquakes(dbSession, params)
    earthquakeCount: dict[str, int] = {}

    for e in earthquakes:
        country: CountryInternal | None
        if (hasattr(e, 'country') and e.country != None):
            country = e.country
        else:
            country = db.check_coordinates_in_country(dbSession, e.latitude, e.longitude)

        if (country != None):
            if (not (country.name in earthquakeCount)):
                earthquakeCount[country.name] = 1
            else:
                earthquakeCount[country.name] += 1

            if (not hasattr(e, 'country') or e.country == None):
                e.country = country
                earthquakeDb.update_earthquakes(dbSession, [e])

    response: list[TopCountryEarthquakeCount] = []
    for key,val in earthquakeCount.items():
        response.append(TopCountryEarthquakeCount(
            name = key,
            count = val,
        ))

    return TopCountryEarthquakeCountResponse(data = sorted(response, key=lambda x: x.count, reverse=True))

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