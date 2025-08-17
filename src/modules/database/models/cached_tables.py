from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Sequence

from config.db.database_base import Base

class CachedTables(Base):
    
    id = Column(Sequence("cached_tables_id_seq"))
    table_name = Column(String())
    field_list = Column()
    interval = ""
    connection = ""
    is_active = False



