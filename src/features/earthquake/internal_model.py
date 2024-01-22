from datetime import datetime
from typing import Optional
from src.features.country.internal_model import CountryInternal

class CreateEarthquakeInternal:
    providerId: str
    date: datetime
    magnitude: float
    latitude: float
    longitude: float
    depth: Optional[float]
    type: Optional[str]
    country: Optional[CountryInternal]

    def __init__(
        self, 
        providerId: str, 
        date: datetime, 
        magnitude: float, 
        latitude: float,
        longitude: float,
        depth: Optional[float] = None, 
        type: Optional[str] = None,
        country: Optional[CountryInternal] = None,
    ):
        self.providerId = providerId
        self.date = date
        self.magnitude = magnitude
        self.latitude = latitude
        self.longitude = longitude
        
        self.depth = depth
        self.type = type
        self.country = country

class EarthQuakeInternal(CreateEarthquakeInternal):
    id: int

    def __init__(
        self, 
        id: int, 
        providerId: str, 
        date: datetime, 
        magnitude: float, 
        latitude: float,
        longitude: float,
        depth: Optional[float] = None, 
        type: Optional[str] = None,
        country: Optional[CountryInternal] = None,
    ):
        self.id = id
        super().__init__(providerId, date, magnitude, latitude, longitude, depth = depth, type = type, country = country)

class EarthquakeByYearInternal:
    year: int
    count: int

    def __init__(self, year: int, count: int):
        self.year = year
        self.count = count
