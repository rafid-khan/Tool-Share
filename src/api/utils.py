from enum import Enum


class SortBy(Enum):
    ASCENDING = 'ASC'
    DESCENDING = 'DESC'


class SortType(Enum):
    NAME = 'p320_24.tool.name '
    CATEGORY = 'p320_24.category.tag_name '
