from typing import Optional
from pydantic import BaseModel, Field, field_validator

class List(BaseModel):

    bitrix_id: Optional[int] = Field(None, alias="ID")
    name: Optional[str] = Field(None, alias="NAME")

    timestamp_x: Optional[str] = Field(None, alias="TIMESTAMP_X")
    partner_url_parametr: Optional[str] = Field(None, alias="PROPERTY_225")
    min_product_cost: Optional[int] = Field(None, alias="PROPERTY_227")
    max_product_cost: Optional[int] = Field(None, alias="PROPERTY_229")
    min_installment_period: Optional[int] = Field(None, alias="PROPERTY_231")
    max_installment_period: Optional[int] = Field(None, alias="PROPERTY_233")
    min_first_payment: Optional[int] = Field(None, alias="PROPERTY_235")
    max_first_payment: Optional[int] = Field(None, alias="PROPERTY_237")
    trade_margin: Optional[int] = Field(None, alias="PROPERTY_239")
    trade_margin_list: Optional[dict] = Field(None, alias="PROPERTY_243")

    # Валидатор для всех полей кроме trade_margin_list
    @field_validator("*", mode="before")
    @classmethod
    def extract_dict_value(cls, v, info):
        if info.field_name == "trade_margin_list":
            return v  # пропускаем поле trade_margin_list
        if isinstance(v, dict):
            return next(iter(v.values()))
        return v

    # Специальный валидатор для trade_margin_list
    @field_validator("trade_margin_list", mode="before")
    @classmethod
    def parse_trade_margin_list(cls, v):
        if not isinstance(v, dict):
            return v
        result = {}
        for value in v.values():
            left, right = value.split(")")
            result[int(left.strip())] = float(right.strip())
        return result