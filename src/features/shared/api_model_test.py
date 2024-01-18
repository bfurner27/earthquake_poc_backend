from .api_model import get_offset_from_page, get_paging
import pytest

class TestGetPaging:
    def test_happy_case(self):
        r = get_paging(1, 10, 5)
        assert r.totalPages == 1

    def test_larger_numbers(self):
        r = get_paging(10, 422, 10234)
        assert r.totalPages == 25

    def test_page_size_0(self):
        with pytest.raises(Exception, match = 'pageSize must be larger than 0 was 0'):
            r = get_paging(1, 0, 5)

    def test_page_0(self):
        with pytest.raises(Exception, match = 'page must be 1 or more, was 0'):
            r = get_paging(0, 10, 5)

class TestGetOffset:
    def test_page_3_size_25(self):
        r = get_offset_from_page(3, 25)
        assert r == 50

    def test_page_1_size_25(self):
        r = get_offset_from_page(1, 25)
        assert r == 0
    
    def test_page_size_0(self):
        with pytest.raises(Exception, match = 'pageSize must be larger than 0 was 0'):
            r = get_offset_from_page(1, 0)

    def test_page_0(self):
        with pytest.raises(Exception, match = 'page must be 1 or more, was 0'):
            r = get_offset_from_page(0, 10)
