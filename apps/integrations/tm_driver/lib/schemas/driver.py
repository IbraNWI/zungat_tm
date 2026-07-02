from datetime import date
from typing import Optional
from pydantic import Field
from .base_config import BaseConfigModel

class Driver(BaseConfigModel):
    id:Optional[int] = Field(None,alias="driver_id")
    name:Optional[str] = Field(None,alias="name")
    balance:Optional[float] = Field(None,alias="balance")
    birthday:Optional[str] = Field(None,alias="birthday")
    tabel_number:Optional[str] = Field(None,alias="number")
    driver_license:Optional[str] = Field(None,alias="driver_license")
    license:Optional[str] = Field(None,alias="license")
    home_phone:Optional[str] = Field(None,alias="home_phone")
    mobile_phone:Optional[str] = Field(None,alias="mobile_phone")
    comment:Optional[str] = Field(None,alias="comment")
