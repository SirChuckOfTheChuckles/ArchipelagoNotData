"""
Helper class for errors-by-value
"""
from typing import Generic, TypeVar

E = TypeVar('E')


class Error(Generic[E]):
    def __init__(self, message: E) -> None:
        self.message = message
    
    def __str__(self) -> str:
        return f"Error({self.message})"

    def __repr__(self) -> str:
        return f"Error({self.message})"
