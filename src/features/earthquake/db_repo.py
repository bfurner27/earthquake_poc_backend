from datetime import datetime
import sys
from typing import Optional
from sqlalchemy import Column, desc, asc
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON
from .transformers import fromDBtoInternal, fromInternalToDB
from src.features.shared.db_repo import OrderBy, ReadParamsBase, Order
from .db_model import Earthquake as DBEarthquake
from .internal_model import EarthQuakeInternal, CreateEarthquakeInternal

class ReadEarthquakeParams(ReadParamsBase):
    minDatetime: datetime | None = None

    def __init__(
        self,     
        offset: int = 0,
        limit: int = 100,
        orderBy: OrderBy | None = None,
        minDatetime: Optional[datetime] = None,
    ):
        self.minDatetime = minDatetime
        super().__init__(offset, limit, orderBy)

def earthquake_count(db: Session):
    return db.query(DBEarthquake).count()

def read_earthquake(db: Session, earthquakeId: int) -> EarthQuakeInternal | None:
    earthquakes = db.query(DBEarthquake).filter(DBEarthquake.id == earthquakeId).all()
    if (len(earthquakes) > 1):
        raise Exception(f'the id specified had multiple enries, should only have one id: {earthquakeId}')
    
    if (len(earthquakes) == 0):
        return None

    return earthquakes[0]

def read_earthquakes(db: Session, params: ReadEarthquakeParams) -> list[EarthQuakeInternal]:
    field: Column = DBEarthquake.id
    sqlOrder = asc
    if (params.orderBy != None):
        fieldRaw = params.orderBy.field
        order = params.orderBy.order
        sqlOrder = asc
        if (order == Order.DESC):
            sqlOrder = desc

        if(fieldRaw == 'id'):
            field = DBEarthquake.id
        elif (fieldRaw == 'magnitude'):
            field = DBEarthquake.magnitude
        elif (fieldRaw == 'date'):
            field = DBEarthquake.date
        else:
            raise Exception(f"unrecognized field passed into the order by {fieldRaw}")
    
    q = db.query(DBEarthquake, DBEarthquake.coordinates_json)

    if (params.minDatetime != None):
        q = q.filter(DBEarthquake.date >= params.minDatetime.strftime('%Y-%m-%d %H:%M:%S'))

    q = q.order_by(sqlOrder(field)).offset(params.offset).limit(params.limit)
    result: list[EarthQuakeInternal] = list()
    for dbEarthquake, coordinate_json in q.all():
        result.append(fromDBtoInternal(dbEarthquake, coordinate_json))
    return result

def create_earthquakes(db: Session, earthquakes: list[CreateEarthquakeInternal]):
    dbEarthquakes = [ fromInternalToDB(e) for e in earthquakes ]

    db.add_all(dbEarthquakes)
    db.commit()

    results: list[EarthQuakeInternal] = []
    for i in range(0, len(dbEarthquakes)):
        db.refresh(dbEarthquakes[i])
        e = dbEarthquakes[i]
        q = db.query(e.coordinates_json)
        data = q.all()[0][0]
        results.append(fromDBtoInternal(e, data))

    return results

def update_earthquakes(db: Session, earthquakes: list[EarthQuakeInternal]):
    for e in earthquakes:
        dbEarthquake = db.query(DBEarthquake).filter(DBEarthquake.id == e.id).first()
        dbEarthquake.providerId = e.providerId
        dbEarthquake.date = e.date
        dbEarthquake.depth = e.depth if hasattr(e, 'depth') else dbEarthquake.depth
        dbEarthquake.magnitude = e.magnitude
        dbEarthquake.type = e.type if hasattr(e, 'type') else dbEarthquake.type
        dbEarthquake.coordinates = f'POINT({e.latitude} {e.longitude})'
        dbEarthquake.countryId = e.country.id if hasattr(e, 'country')  else None
        
        db.commit()

    return earthquakes

def delete_earthquakes(db: Session, ids: list[int]):
    for id in ids:
        db.query(DBEarthquake).filter(DBEarthquake.id == id).delete()

    return