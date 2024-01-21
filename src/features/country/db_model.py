from geoalchemy2 import Geography
from src.features.earthquake.db_model import Earthquake
from src.utils.db import ORMBase
from sqlalchemy import Column, INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship

class Country(ORMBase):
    __tablename__ = 'countries'

    id = Column(INTEGER, autoincrement=True, primary_key=True, nullable=False)
    name = Column(VARCHAR(150), nullable=False)
    requestId = Column(VARCHAR(100), nullable=False)
    boundaries = Column(Geography(from_text='ST_GeomFromGeoJSON'))
    modified = Column(TIMESTAMP, server_onupdate=current_timestamp(), server_default=current_timestamp())
    created = Column(TIMESTAMP, server_default=current_timestamp(), nullable=False)

    earthquakes = relationship(Earthquake, back_populates = 'country')