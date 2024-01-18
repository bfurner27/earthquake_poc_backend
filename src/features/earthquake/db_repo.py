from sqlalchemy import desc, asc
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON
from src.features.shared.db_repo import ReadParamsBase, Order
from .db_model import Earthquake as DBEarthquake
from .internal_model import EarthQuakeInternal, CreateEarthquakeInternal
from json import loads

class ReadEarthquakeParams(ReadParamsBase):
    pass

def earthquake_count(db: Session):
    return db.query(DBEarthquake).count()

def read_earthquake(db: Session, earthquakeId: int) -> EarthQuakeInternal | None:
    earthquakes = db.query(DBEarthquake).filter(id == earthquakeId).all()
    if (len(earthquakes) > 1):
        raise Exception(f'the id specified had multiple enries, should only have one id: {earthquakeId}')
    
    if (len(earthquakes) == 0):
        return None

    return earthquakes[0]

def read_earthquakes(db: Session, params: ReadEarthquakeParams) -> list[EarthQuakeInternal]:
    q = db.query(DBEarthquake, DBEarthquake.coordinates_json).offset(params.offset).limit(params.limit)
    if (params.orderBy != None):
        field = params.orderBy.field
        order = params.orderBy.order
        sqlOrder = asc
        if (order == Order.DESC):
            sqlOrder = desc
        q.order_by(field, sqlOrder)

    result: list[EarthQuakeInternal] = list()
    for dbEarthquake, coordinate_json in q.all():
        coordinates = loads(coordinate_json).get('coordinates', [None, None])
        country = EarthQuakeInternal(
            dbEarthquake.id, 
            dbEarthquake.providerId, 
            dbEarthquake.date, 
            dbEarthquake.magnitude,
            coordinates[0],
            coordinates[1], 
            depth = dbEarthquake.depth, 
            type = dbEarthquake.type
        )
        result.append(country)
    return result

def create_earthquakes(db: Session, earthquakes: list[CreateEarthquakeInternal]):
    dbEarthquakes = [ DBEarthquake(
        providerId = e.providerId, 
        date = e.date, 
        depth = e.depth if hasattr(e, 'depth') else None, 
        magnitude = e.magnitude, 
        type = e.type if hasattr(e, 'type') else None, 
        coordinates = f'POINT({e.latitude} {e.longitude})'
    ) for e in earthquakes ]   

    db.add_all(dbEarthquakes)
    db.commit()

    results: list[EarthQuakeInternal] = []
    for i in range(0, len(dbEarthquakes)):
        db.refresh(dbEarthquakes[i])
        e = dbEarthquakes[i]
        q = db.query(e.coordinates_json)
        data = q.all()[0][0]
        jsonData = loads(data)
        rawCoordinates = jsonData.get('coordinates', [None, None])
        results.append(EarthQuakeInternal(
        e.id, 
        e.providerId, 
        e.date, 
        e.magnitude, 
        rawCoordinates[0], 
        rawCoordinates[1], 
        depth = e.depth if hasattr(e, 'depth') else None, 
        type = e.type if hasattr(e, 'type') else None,
    ))

    return results

def update_earthquakes(db: Session, earthquakes: list[EarthQuakeInternal]):
    for e in earthquakes:
        db.query(DBEarthquake).filter(id == e.id).update(DBEarthquake(
            providerId = e.providerId, 
            date = e.date, 
            depth = e.depth if hasattr(e, 'depth') else None, 
            magnitude = e.magnitude, 
            type = e.type if hasattr(e, 'type') else None, 
            coordinates = e.coordinates
        ))
        db.commit()

    return earthquakes

def delete_earthquakes(db: Session, ids: list[int]):
    for id in ids:
        db.query(DBEarthquake).filter(DBEarthquake(id = id)).delete()

    return