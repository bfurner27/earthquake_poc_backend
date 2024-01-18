from typing import Optional

class Boundaries:
    coordinates: list
    type: str

    def __init__(self, coordinates: list, boundaryType: str):
        self.coordinates = coordinates
        self.type = boundaryType

class CreateCountryInternal:
    requestId: str
    name: str
    boundaries: Boundaries

    def __init__(self, name: str, boundaries: Boundaries, requestId: str):
        self.name = name
        self.boundaries = boundaries
        self.requestId = requestId

class CountryInternal(CreateCountryInternal):
    id: int

    def __init__(self, id: int, name: str, boundaries: Boundaries, requestId: str):
        self.id = id
        super().__init__(name, boundaries, requestId)