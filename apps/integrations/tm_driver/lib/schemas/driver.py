from datetime import date
from typing import Optional
from pydantic import Field
from .base_config import BaseConfigModel

class Driver(BaseConfigModel):
    id:Optional[int] = Field(None,alias="driver_id")
    name:Optional[str] = Field(None,alias="name")
    balance:Optional[float] = Field(None,alias="balance")
    birthday:Optional[date] = Field(None,alias="birthday")
    tabel_number:Optional[str] = Field(None,alias="number")
    driver_license:Optional[str] = Field(None,alias="driver_license")
    license:Optional[str] = Field(None,alias="license")
    home_phone:Optional[str] = Field(None,alias="home_phone")
    mobile_phone:Optional[str] = Field(None,alias="mobile_phone")
    comment:Optional[str] = Field(None,alias="comment")


{
    'driver_id': 3405, 
    'name': 'Картоев Ибрагим Вахаевич', 
    'balance': 140.41, 
    'birthday': None, 
    'number': '', 
    'car_id': 3578, 
    'driver_license': '0 полная оплата, рассрочка зунгат, документ 0000-002750, с 04.12.2022, на 61дней, платил хорошо', 
    'license': '', 
    'home_phone': '', 
    'mobile_phone': '89290010006', 
    'is_locked': False, 
    'is_dismissed': False, 
    'self_employed': False, 
    'individual_entrepreneur': False, 
    'inn': '', 
    'insurance_number': '', 
    'time_block': None, 
    'temporary_block_reason': '', 
    'order_params': [], 
    'attribute_values': [], 
    'phones': [
        {'phone': '89290010006', 'is_default': True, 'use_for_call': True}
        ], 
    'term_account': '03405', 
    'name_for_taxophone': '', 
    'accounts': [
        {
            'account_kind': 0, 
            'balance': 140.41
            }
        ], 
    'kpi': 0, 
    'uds_id': 0, 
    'passport': 'Магас', 
    'employee_type': 0, 
    'start_date': '20171201000000', 
    'lic_date': None, 
    'comment': 'Не нажимает вовремя "ПОЕХАЛИ" (+2)\r\nРаньше времени нажал "НА МЕСТЕ" (+)\r\n+1 Выполнил заказ по пути\r\n+2 Не вышел на предварительный заказ\r\nрассрочка зунгат, документ 0000-002750, с 04.12.2022, на 61дней\r\n0 полная оплата, рассрочка зунгат, документ 0000-002750, с 04.12.2022, на 61дней, платил хорошо', 
    'email': ''}