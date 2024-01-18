from typing import Annotated
from fastapi import Body
from pydantic import BaseModel, Field
from enum import Enum

from src.features.shared.api_model import ApiResponse, ApiRequest

class AllowedShapeTypes(str, Enum):
    multipolygon = 'MULTIPOLYGON'
    polygon = 'POLYGON'

class CountryBaseOutput(BaseModel):
    id: int | None
    name: str

class CountryValidateOutput(CountryBaseOutput):
    requestId: str

class CountryValidateOutputData(ApiResponse):
    data: list[CountryValidateOutput]
    errors: list[CountryValidateOutput]

class CountryOutput(CountryBaseOutput):
    coordinates: list
    shapeType: AllowedShapeTypes

class CountryOutputData(ApiResponse):
    data: list[CountryOutput]

class CountryCreate(BaseModel):
    requestId: str
    name: str
    coordinates: Annotated[list, Field(examples=[
        [[
            [[1,-1], [-1,-1], [-1, 1], [1, 1]]
        ]]
    ])]
    shapeType: AllowedShapeTypes

class CountryCreateInput(ApiRequest):
    data: Annotated[list[CountryCreate], Field(max_length = 100)]