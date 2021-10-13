from sqlalchemy import Column, Index, BigInteger, Integer, String, DateTime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()
ReflectModel = automap_base()


class SomeModel(BaseModel):
    __tablename__ = "some_table"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type = Column(Integer, nullable=False, comment="Type")
    name = Column(String(100), nullable=False, comment="Name")
    add_time = Column(DateTime, nullable=False, comment="Add Time")
    __table_args__ = (
        Index("type", "type"),
    )
