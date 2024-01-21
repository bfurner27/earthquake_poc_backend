from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_AsGeoJSON
from src.utils.db import ORMBase
from sqlalchemy import Column, INTEGER, VARCHAR, TIMESTAMP, FLOAT, ForeignKey, Integer
from sqlalchemy.sql.functions import current_timestamp
from json import loads
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship;

class Earthquake(ORMBase):
    __tablename__ = 'earthquakes'

    id = Column(INTEGER, autoincrement=True, primary_key=True, nullable=False)
    providerId = Column(VARCHAR(100))
    date = Column(TIMESTAMP, nullable=False)
    depth = Column(FLOAT)
    magnitude = Column(FLOAT, nullable=False)
    type = Column(VARCHAR(100))
    coordinates = Column(Geometry('POINT'))
    modified = Column(TIMESTAMP, server_onupdate=current_timestamp(), server_default=current_timestamp())
    created = Column(TIMESTAMP, server_default=current_timestamp(), nullable=False)
    countryId = Column(INTEGER, ForeignKey('countries.id'), nullable=True)

    country = relationship('Country', back_populates = 'earthquakes')

    @hybrid_property
    def coordinates_json(self) -> str:
        return ST_AsGeoJSON(self.coordinates)