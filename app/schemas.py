from pydantic import BaseModel

class Price(BaseModel):
    ticker: str
    price: float
    timestamp: int