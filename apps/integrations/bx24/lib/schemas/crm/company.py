from typing import Optional, List
from pydantic import Field

from apps.integrations.bx24.lib.schemas.crm.base_model import BaseConfigModel, CustomField



class Company(BaseConfigModel):
    id:Optional[int] = Field(None,alias="ID")