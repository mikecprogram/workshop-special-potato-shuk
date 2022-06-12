from typing import Generic, TypeVar

T = TypeVar("T")
class Response(Generic[T]):
    def __init__(self, response:T = None ,exception : str= None):
        self.isexc:bool = exception is not None
        self.res:T = response
        self.exc:str = exception