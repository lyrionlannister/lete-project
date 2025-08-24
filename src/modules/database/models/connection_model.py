# connection_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Sequence
from sqlalchemy.orm import relationship
from config.db.database_base import Base


class ConnectionModel(Base):
    __tablename__ = "connections"

    id = Column(Integer, Sequence("connection_id_seq"), primary_key=True)
    name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    user = Column(String, nullable=False)
    password = Column(String, nullable=False)
    database = Column(String, nullable=False)
    ssl_enabled = Column(Boolean, default=False)
    sql_engine = Column(String, nullable=False)

    # relación inversa
    cached_tables = relationship("CachedTablesModel", back_populates="connection", cascade="all, delete-orphan")
