from math import ceil
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.features.shared.api_model import Paging, get_offset_from_page, get_paging

from .internal_model import CreateEarthquakeInternal, EarthQuakeInternal
from .api_model import EarthQuakeOutput, EarthQuakeOutputData, EarthquakeCreateData, EarthquakeCreateInput, EarthquakeOutputWPagingData
from ..earthquake import db_repo as db
from src.features.shared.dependencies import get_db

router = APIRouter()

@router.get('')
def read_earthquakes(
    page: Annotated[int, Query(min = 1)] = 1, 
    pageSize: Annotated[int, Query(max = 100, min = 1)] = 100, 
    dbSession: Session = Depends(get_db),
) -> EarthquakeOutputWPagingData:
    totalRecords = db.earthquake_count(dbSession)
    offset = get_offset_from_page(page, pageSize)
    paging = get_paging(page, pageSize, totalRecords)
    
    if (offset == 0 and paging.totalRecords == 0):
        return EarthquakeOutputWPagingData(
            data = [], 
            paging = paging,
        )

    if (offset != 0 and offset > paging.totalRecords):
        raise HTTPException(status_code=422, detail='offset is more than total entries available')

    results = db.read_earthquakes(dbSession, db.ReadEarthquakeParams(offset = offset, limit = pageSize))

    return EarthquakeOutputWPagingData(
        data = [ EarthQuakeOutput(
            providerId = e.providerId,
            date = e.date,
            depth = e.depth if hasattr(e, 'depth') else None,
            magnitude = e.magnitude,
            type = e.type if hasattr(e, 'type') else None,
            latitude = e.latitude,
            longitude = e.longitude,
            id = e.id,
        ) for e in results],
        paging = paging,
    )

@router.get('/{id}')
def read_earthquake(id: int, dbSession: Session = Depends(get_db)) -> EarthQuakeOutputData:
    earthquake = db.read_earthquake(dbSession, id)
    if (earthquake == None):
        return EarthQuakeOutputData(data = [])

    return EarthQuakeOutputData(data = [ earthquake ])

@router.post('')
def create_earthquake(body: EarthquakeCreateData, dbSession: Session = Depends(get_db)) -> EarthQuakeOutputData:
    input_data = body.data
    results = db.create_earthquakes(dbSession, [CreateEarthquakeInternal(
        e.providerId,
        e.date,
        e.magnitude,
        e.latitude, 
        e.longitude,
        e.depth,
        e.type,
    ) for e in input_data])

    return EarthQuakeOutputData(data = [ EarthQuakeOutput(
        providerId = e.providerId,
        date = e.date,
        depth = e.depth if hasattr(e, 'depth') else None,
        magnitude = e.magnitude,
        type = e.type if hasattr(e, 'type') else None,
        latitude = e.latitude,
        longitude = e.longitude,
        id = e.id,
    ) for e in results])

@router.put('/{id}')
def update_earthquake(id: int, body: EarthquakeCreateInput, dbSession: Session = Depends(get_db)) -> EarthQuakeOutputData:
    updates = db.update_earthquakes(dbSession, [EarthQuakeInternal(
        id,
        body.providerId,
        body.date,
        body.magnitude,
        body.latitude,
        body.longitude,
        depth = body.depth if hasattr(body, 'depth') else None,
        type = body.type if hasattr(body, 'type') else None,
    )])

    return  EarthQuakeOutputData(
        data = [ EarthQuakeOutput(
            id = u.id, 
            providerId = u.providerId, 
            date = u.date, 
            depth = u.depth if hasattr(u, 'depth') else None,
            magnitude = u.magnitude,
            type = u.type if hasattr(u, 'type') else None,
            latitude = u.latitude,
            longitude = u.longitude,
        ) for u in updates ]
    )

@router.delete('/{id}')
def delete_earthquake(id: int, dbSession: Session = Depends(get_db)):
    db.delete_earthquakes(dbSession, [id])