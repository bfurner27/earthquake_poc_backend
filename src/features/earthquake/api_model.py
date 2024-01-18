from pydantic import BaseModel
from datetime import datetime
from src.features.shared.api_model import ApiResponse, ApiRequest, ApiResponseWPaging

class EarthquakeBaseModel(BaseModel):
    providerId: str
    date: datetime
    depth: float | None = None
    magnitude: float
    type: str | None = None
    latitude: float
    longitude: float

class EarthquakeCreateInput(EarthquakeBaseModel):
    pass

class EarthquakeCreateData(ApiRequest):
    data: list[EarthquakeCreateInput]

class EarthQuakeOutput(EarthquakeBaseModel):
    id: int

class EarthQuakeOutputData(ApiResponse):
    data: list[EarthQuakeOutput]

class EarthquakeOutputWPagingData(ApiResponseWPaging):
    data: list[EarthQuakeOutput]





