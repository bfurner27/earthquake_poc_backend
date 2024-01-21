from json import loads
from .internal_model import EarthQuakeInternal
from .db_model import Earthquake as DBEarthquake

def fromDBtoInternal(obj: DBEarthquake, coordinate_json: str) -> EarthQuakeInternal:
    coordinates = loads(coordinate_json).get('coordinates', [None, None])

    return EarthQuakeInternal(
        obj.id, 
        obj.providerId, 
        obj.date, 
        obj.magnitude, 
        coordinates[0], 
        coordinates[1], 
        obj.depth, 
        obj.type, 
        obj.country,
    )

def fromInternalToDB(e: EarthQuakeInternal) -> DBEarthquake:
    return DBEarthquake(
        providerId = e.providerId, 
        date = e.date, 
        depth = e.depth if hasattr(e, 'depth') else None, 
        magnitude = e.magnitude, 
        type = e.type if hasattr(e, 'type') else None, 
        coordinates = f'POINT({e.latitude} {e.longitude})',
        countryId = e.country.id if hasattr(e, 'country') else None,
    )