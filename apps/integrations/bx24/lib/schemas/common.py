from __future__ import annotations

from datetime import datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class BitrixTimeInfo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    start: Optional[float] = None
    finish: Optional[float] = None
    duration: Optional[float] = None
    processing: Optional[float] = None

    date_start: Optional[datetime] = Field(None, alias="date_start")
    date_finish: Optional[datetime] = Field(None, alias="date_finish")


class BitrixResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    result: Optional[T] = None
    time: Optional[BitrixTimeInfo] = None

    error: Optional[str] = None
    error_description: Optional[str] = None

    def raise_for_error(self):
        if self.error:
            raise RuntimeError(f"{self.error}: {self.error_description}")
