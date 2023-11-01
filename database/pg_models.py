# from sqlalchemy import Column, Integer, String
from typing import List

from shapely import Polygon
from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import CITEXT, JSONB
from geoalchemy2 import Geography
import datetime
import uuid

PG_BASE = declarative_base()

class SpatialRefSys(PG_BASE):
    __tablename__ = "spatial_ref_sys"

    srid: Mapped[int] = mapped_column(primary_key=True)
    geography: Mapped[List["CustomGeography"]] = relationship(back_populates="srid")
class TimeStampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    last_updated: Mapped[datetime.datetime] = mapped_column(onupdate=func.now())


class CustomGeography(TimeStampMixin, PG_BASE):
    __tablename__ = "custom_geography"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    meta: Mapped[dict] = mapped_column(type_=JSONB, default=None)
    geography: Mapped[Polygon] = mapped_column(type_=Geography(geometry_type="POLYGON"), nullable=False)
    input_srid: Mapped[int] = mapped_column(ForeignKey("spatial_ref_sys.srid"), nullable=False)

    srid: Mapped["SpatialRefSys"] = relationship(back_populates="custom_geography")


class User(TimeStampMixin, PG_BASE):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    oauth_id: Mapped[str] = mapped_column(nullable=False)
    meta: Mapped[dict] = mapped_column(type_=JSONB, default=None)



