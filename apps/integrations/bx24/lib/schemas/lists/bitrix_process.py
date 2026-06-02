# from __future__ import annotations

# from typing import Dict, Optional

# from pydantic import BaseModel, ConfigDict, Field


# class BXList(BaseModel):
#     model_config = ConfigDict(extra="allow", populate_by_name=True)

#     id: Optional[int] = Field(None, alias="ID")
#     name: Optional[str] = Field(None, alias="NAME")
#     code: Optional[str] = Field(None, alias="CODE")

#     iblock_type_id: Optional[str] = Field(None, alias="IBLOCK_TYPE_ID")
#     site_id: Optional[str] = Field(None, alias="LID")


# class BXListElement(BaseModel):
#     model_config = ConfigDict(extra="allow", populate_by_name=True)

#     id: Optional[int] = Field(None, alias="ID")
#     iblock_id: Optional[int] = Field(None, alias="IBLOCK_ID")

#     name: Optional[str] = Field(None, alias="NAME")

#     # PROPERTY_* автоматически попадут в extra


from pydantic import Field
from apps.integrations.bx24.lib.schemas.lists.base_model import BaseConfigModel




class BitrixProcess(BaseConfigModel):
    ...
    