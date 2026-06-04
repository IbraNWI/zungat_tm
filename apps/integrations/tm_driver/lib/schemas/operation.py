from datetime import datetime
from typing import Optional
from pydantic import Field
from .base_config import BaseConfigModel

class Operation(BaseConfigModel):
    id:Optional[int] = Field(None,alias="oper_id")
    driver_id:Optional[int] = Field(None,alias="driver_id")
    title:Optional[str] = Field(None,alias="name")
    create_time:Optional[datetime] = Field(None,alias="oper_time")
    sum:Optional[float] = Field(None,alias="sum")
    oper_sum:Optional[float] = Field(None,alias="oper_sum")
    oper_type:Optional[str] = Field(None,alias="oper_type")
    comment:Optional[str] = Field(None,alias="comment")
    account_type:Optional[int] = Field(None,alias="account_kind")
    cancelled_by_oper_id:Optional[int] = Field(None,alias="cancelled_by_oper_id")
    cancelled_oper_id:Optional[int] = Field(None,alias="cancelled_oper_id")
    