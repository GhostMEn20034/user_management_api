import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class PaginationParams:
    page: int
    page_size: int

    def get_offset_and_limit(self) -> Tuple[int, int]:
        """
        :return: Offset (first tuple value), limit (the second one)
        """
        offset = (self.page - 1) * self.page_size
        limit = self.page_size

        return offset, limit

    def get_total_pages(self, total_count: int):
        """
        :param total_count: Total number of items returned
        """
        total_pages = math.ceil(total_count / self.page_size)
        # By default, pagination should always result
        # in at least one "page" (even if it's empty), so this block of code ensures that total_pages is at least 1.
        if total_pages < 1:
            total_pages = 1

        return total_pages


@dataclass
class PaginationResponse:
    current_page: int
    page_size: int
    total_pages: int
    total_items: int

    def model_dump(self) -> dict[str, int]:
        return {
            "current_page": self.current_page,
            "page_size": self.page_size,
            "total_pages": self.total_pages,
            "total_items": self.total_items,
        }
