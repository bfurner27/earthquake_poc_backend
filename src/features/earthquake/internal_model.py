from datetime import datetime
from typing import Optional

class CreateEarthquakeInternal:
    providerId: str
    date: datetime
    magnitude: float
    latitude: float
    longitude: float
    depth: Optional[float]
    type: Optional[str]

    def __init__(
        self, 
        providerId: str, 
        date: datetime, 
        magnitude: float, 
        latitude: float,
        longitude: float,
        depth: Optional[float] = None, 
        type: Optional[str] = None
    ):
        self.providerId = providerId
        self.date = date
        self.magnitude = magnitude
        self.latitude = latitude
        self.longitude = longitude

        if (depth != None):
            self.depth = depth

        if (type != None):
            self.type = type

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
        type: Optional[str] = None
    ):
        self.id = id
        super().__init__(providerId, date, magnitude, latitude, longitude, depth = depth, type = type)