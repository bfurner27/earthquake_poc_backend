from json import dumps
from typing import Optional
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from .db_model import Country as DBCountry
from .internal_model import CountryInternal, CreateCountryInternal
from src.features.shared.db_repo import ReadParamsBase

class ReadCountryParams(ReadParamsBase):
    pass


def read_countries(db: Session, params: ReadCountryParams) -> list[CountryInternal]:
    q = db.query(DBCountry).offset(params.offset).limit(params.limit)
    if (params.orderBy != None):
        name, order = params.orderBy
        q.order_by(name, order)

    result: list[CountryInternal] = list()
    for dbCountry in q.all():
        country = CountryInternal(dbCountry.id, dbCountry.name, dbCountry.boundaries)
        result.append(country)
    return result


def read_country(db: Session, id: int) -> Optional[CountryInternal]:
    result = read_countries(db, ReadCountryParams(id = id))
    if (len(result)  > 1):
        raise Exception(f'more than one entry found for the country id {id}')
    
    if (len(result) == 1):
        return result[0]
    
    return None

def create_countries(db: Session, countries: list[CreateCountryInternal]) -> list[CountryInternal]:
    dbCountries = [ DBCountry(
        requestId = country.requestId,
        name = country.name, 
        boundaries = dumps({ 'type': country.boundaries.type, 'coordinates': country.boundaries.coordinates})
    ) for country in countries ]
    db.add_all(dbCountries)
    db.commit()
    for i in range(0, len(dbCountries)):
        db.refresh(dbCountries[i])

    return [CountryInternal(country.id, country.name, country.boundaries, country.requestId) for country in dbCountries]

def create_country(db: Session, country: CreateCountryInternal) -> Optional[CountryInternal]:
    data = create_countries(db, [country])
    if (len(data) == 0):
        return None
    
    return data[0]

def update_countries(db: Session, countries: list[CountryInternal]) -> list[CountryInternal]:
    for country in countries:
        db.query(DBCountry).filter(id == country.id).update(DBCountry(name = country.name, boundaries = country.boundaries))
        db.commit()

    return countries

def update_country(db: Session, country: CountryInternal) -> Optional[CountryInternal]:
    data = update_countries(db, [country])
    if (len(data) == 0):
        return None
    
    return data[0]

def delete_countries(db: Session, ids: list[int]):
    for id in ids:
        db.query(CountryInternal).filter(DBCountry(id = id)).delete()

    return

def delete_country(db: Session, id: int):
    delete_countries(db, [id])
