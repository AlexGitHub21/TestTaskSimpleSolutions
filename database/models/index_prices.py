from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric
from database.models.base import Base

class IndexPrices(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
