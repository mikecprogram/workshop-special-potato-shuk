from typing import Generic, TypeVar

T = TypeVar("T")
class Response(Generic[T]):
    def __init__(self, response:T = None ,exception : str= None):
        self.is_exception:bool = exception is not None
        self.response:T = response
        self.exception:str = exception