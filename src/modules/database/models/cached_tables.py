# cached_tables_model.py
from sqlalchemy import Column, Integer, String, Sequence, Boolean, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from config.db.database_base import Base


class CachedTablesModel(Base):
    __tablename__ = "cached_tables"

    id = Column(Integer, Sequence("cached_tables_id_seq"), primary_key=True, autoincrement=True)
    table_name = Column(String(), nullable=False)
    field_list = Column(ARRAY(String))
    interval = Column(String)
    connection_id = Column(Integer, ForeignKey("connections.id"), nullable=False)  # FK
    is_active = Column(Boolean, default=False)
    primary_key = Column(String, nullable=False)

    # relación con ConnectionModel
    connection = relationship("ConnectionModel", back_populates="cached_tables")
