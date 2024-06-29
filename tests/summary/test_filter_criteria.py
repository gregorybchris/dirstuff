from dirstuff.summary.filter_criteria import FilterCriteria


class TestFilterCriteria:
    def test_construct_filter_criteria(self) -> None:
        filter_criteria = FilterCriteria(min_bytes=100)
        assert filter_criteria.min_bytes == 100
