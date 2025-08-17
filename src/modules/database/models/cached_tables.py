from sqlalchemy import Column, Integer, String, Sequence, Boolean, ARRAY
from config.db.database_base import Base

class CachedTablesModel(Base):
    __tablename__ = "cached_tables"

    id = Column(Integer, Sequence("cached_tables_id_seq"), primary_key=True, autoincrement=True)
    table_name = Column(String())
    field_list = Column(ARRAY(String))
    interval = Column(String)
    connection = Column(String)
    is_active = Column(Boolean, default=False)