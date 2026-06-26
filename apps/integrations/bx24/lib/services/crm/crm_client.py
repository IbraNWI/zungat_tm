from apps.integrations.bx24.lib.schemas.crm.base_model import BaseConfigModel
from apps.integrations.bx24.lib.schemas.crm.contact import Contact
from apps.integrations.bx24.lib.schemas.crm.lead import Lead
from apps.integrations.bx24.lib.schemas.crm.deal import Deal
from apps.integrations.bx24.lib.schemas.crm.company import Company
from apps.integrations.bx24.lib.schemas.crm.smart_process.payment_rule import PaymentRule
from apps.integrations.bx24.lib.schemas.crm.smart_process.fact_payment import FactPayment
from apps.integrations.bx24.lib.schemas.crm.smart_process.plan_payment import PlanPayment
from apps.integrations.bx24.lib.schemas.crm.timeline_message import TimelineMessage

class CRMTimelineClient:
    def __init__(
            self,
            client,
            entity_type_id):
        self.client = client
        self.entity_type_id = entity_type_id
        self.endpoint = "crm.timeline.logmessage"
    
    def get(self,id:int):
        method = f"{self.endpoint}.get"
        params = {
            "id":id
            }
        response = self.client._request(method=method,params=params)["result"]["logMessage"]
        message = TimelineMessage(**response)
        return message

    def add(self,timeline_message:TimelineMessage):
        timeline_message.entity_type_id = self.entity_type_id
        method = f"{self.endpoint}.add"
        params = {
            "fields":timeline_message.dict(by_alias=True,exclude_none=True)
            }
        response = self.client._request(method=method,params=params)["result"]["logMessage"]
        message = TimelineMessage(**response)
        return message

    def delete(self,id:int):
        method = f"{self.endpoint}.delete"
        params = {
            "id":id
            }
        response = self.client._request(method=method,params=params)["result"]["logMessage"]
        message = TimelineMessage(**response)
        return message 

    def list(self):
        method = f"crm.timeline.icon.list"
        params = {}
        response = self.client._request(method=method,params=params)["result"]["icons"]
        return response



class BaseCRMClient:
    
    def __init__(
            self, 
            client, 
            pydantic_class,
            entity_type_id:int
            ):
        self.client = client
        self.pydantic_class = pydantic_class
        self.entity_type_id = entity_type_id
        self.endpoint = "item"
    
    def get(self,entity_id:int):
        method = f"crm.{self.endpoint}.get.json"
        params = {
            "entityTypeId":self.entity_type_id,
            "id":entity_id
            }
        response = self.client._request(method=method,params=params)
        if response is None:
            return response
        entity = self.pydantic_class(**response["result"]["item"])
        return entity
    
    def iter_list(
            self,
            filters: dict | None = None,
            select: list[str] | None = None,
            order: dict | None = None,
            ):
        method = f"crm.{self.endpoint}.list.json"

        params = {
            "entityTypeId": self.entity_type_id,
        }

        if filters:
            params["filter"] = self._convert_filter_keys(filters)

        if select:
            params["select"] = select

        if order:
            params["order"] = order

        start = 0

        while True:
            params["start"] = start

            response = self.client._request(
                method=method,
                params=params,
            )

            if not response:
                return

            result = response["result"]

            for item in result.get("items", []):
                yield self.pydantic_class(**item)

            if "next" not in result:
                return

            start = result["next"]

    def list(self,filters:dict={}):
        method = f"crm.{self.endpoint}.list.json"
        params = {
            "entityTypeId": self.entity_type_id,
            "filter": self._convert_filter_keys(filters)
            }
        response = self.client._request(method=method,params=params)
        if response is None:
            return []
        else:
            response = response["result"]["items"]
        
        entities = [self.pydantic_class(**item) for item in response]
        return entities
    
    def add(self,object:BaseConfigModel):
        method = f"crm.{self.endpoint}.add.json"
        params = {
            "entityTypeId":self.entity_type_id,
            "fields":object.dict(by_alias=True,exclude_none=True)
            }
        response = self.client._request(method=method,params=params)
        if response is None:
            return response
        entity = self.pydantic_class(**response["result"]["item"])
        return entity
    

    def update(self,object:BaseConfigModel):
        method = f"crm.{self.endpoint}.update.json"
        id = object.id
        object.id = None
        params = {
            "entityTypeId":self.entity_type_id,
            "id":id,
            "fields":object.dict(by_alias=True,exclude_none=True)
            }
        response = self.client._request(method=method,params=params)
        if response is None:
            return response
        entity = self.pydantic_class(**response["result"]["item"])
        return entity
    
    def delete(self,entity_id:int):
        method = f"crm.{self.endpoint}.delete.json"
        params = {
            "entityTypeId":self.entity_type_id,
            "id":entity_id
            }
        return self.client._request(method=method,params=params)

    def fields(self):
        method = f"crm.{self.endpoint}.fields.json"
        params = {
            "entityTypeId":self.entity_type_id
            }
        return self.client._request(method=method,params=params)

    def _convert_filter_keys(self, filters: dict) -> dict:
        BITRIX_OPERATORS = (
            "!@", ">=", "<=",
            "=%",  ">",  "<",
            "!",   "%",  "@",)
        result = {}

        for key, value in filters.items():
            operator = ""
            field_name = key

            for op in BITRIX_OPERATORS:
                if key.startswith(op):
                    operator = op
                    field_name = key[len(op):]
                    break

            field = self.pydantic_class.model_fields.get(field_name)

            if field:
                field_name = field.alias or field_name

            result[f"{operator}{field_name}"] = value

        return result


class LeadClient(BaseCRMClient):
    def __init__(self, client):
        super().__init__(client,pydantic_class=Lead,entity_type_id="1")

class DealClient(BaseCRMClient):
    def __init__(self, client):
        self.timeline = CRMTimelineClient(client,entity_type_id="2")
        super().__init__(client,pydantic_class=Deal, entity_type_id="2")

class ContactClient(BaseCRMClient):
    def __init__(self, client):
        self.timeline = CRMTimelineClient(client,entity_type_id="3")
        super().__init__(client,pydantic_class=Contact,entity_type_id="3")

class CompanyClient(BaseCRMClient):
    def __init__(self, client):
        self.timeline = CRMTimelineClient(client,entity_type_id="4")
        super().__init__(client, pydantic_class=Company, entity_type_id="4")

class PaymentRuleClient(BaseCRMClient):
    def __init__(self, client):
        self.timeline = CRMTimelineClient(client,entity_type_id="1064")
        super().__init__(client, pydantic_class=PaymentRule, entity_type_id="1064")

class FactFapymentClient(BaseCRMClient):
    def __init__(self, client):
        self.timeline = CRMTimelineClient(client,entity_type_id="1052")
        super().__init__(client, pydantic_class=FactPayment, entity_type_id="1052")

class PlanPaymentClient(BaseCRMClient):
    def __init__(self, client):
        self.timeline = CRMTimelineClient(client,entity_type_id="1048")
        super().__init__(client, pydantic_class=PlanPayment, entity_type_id="1048")


