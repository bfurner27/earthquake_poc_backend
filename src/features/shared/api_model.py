from math import ceil
from fastapi import HTTPException
from pydantic import BaseModel

class ApiResponse(BaseModel):
    data: list
    errors: list[str] | None = None

class ApiRequest(BaseModel):
    data: list

class Paging(BaseModel):
    totalPages: int
    totalRecords: int
    page: int
    pageSize: int
    
class ApiResponseWPaging(ApiResponse):
    paging: Paging

def get_paging(page: int, pageSize: int, totalRecords: int) -> Paging:
    if (page < 1):
        raise Exception(f'page must be 1 or more, was {page}')

    if (pageSize < 1):
        raise Exception(f'pageSize must be larger than 0 was {pageSize}')

    totalPages = ceil(totalRecords / pageSize)
    return Paging(page = page, totalPages = totalPages, totalRecords = totalRecords, pageSize = pageSize)

def get_offset_from_page(page: int, pageSize: int) -> int:
    """
    takes page information and converts it into an offset (db starting point)

    page - assumes that page will be 1+
    pageSize - the number of records to be included in a page
    """

    if (page < 1):
        raise Exception(f'page must be 1 or more, was {page}')

    if (pageSize < 1):
        raise Exception(f'pageSize must be larger than 0 was {pageSize}')

    return (page - 1) * pageSize