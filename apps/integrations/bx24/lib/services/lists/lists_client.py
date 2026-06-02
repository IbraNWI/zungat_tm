from apps.integrations.bx24.lib.schemas.lists.list import List
from apps.integrations.bx24.lib.schemas.lists.list_socnet import ListSocnet
from apps.integrations.bx24.lib.schemas.lists.bitrix_process import BitrixProcess

class BaseListsClient:
    
    def __init__(
        self,
        client,
        pydantic_class,
        iblock_type_id: str,
        iblock_id: int,
    ):
        self.client = client
        self.pydantic_class = pydantic_class
        self.iblock_type_id = iblock_type_id
        self.iblock_id = iblock_id

    def get(self, element_id: int):
        method = "lists.element.get.json"
        params = {
            "IBLOCK_TYPE_ID": self.iblock_type_id,
            "IBLOCK_ID": self.iblock_id,
            "ELEMENT_ID": element_id,
        }

        response = self.client._request(method=method, params=params)["result"]
        if len(response) > 0:
            response = response[0]
            response = self.pydantic_class(**response)
        else:
            return None
        return response

    # def list(self, filters: dict = None):
    #     method = "lists.element.get.json"

    #     params = {
    #         "IBLOCK_TYPE_ID": self.iblock_type_id,
    #         "IBLOCK_ID": self.iblock_id,
    #         "FILTER": filters or {},
    #     }

    #     response = self.client._request(method=method, params=params)

    #     items = response.get("result", [])

    #     return [self.pydantic_class(**item) for item in items]

    # def add(self, obj):
    #     method = "lists.element.add.json"

    #     params = {
    #         "IBLOCK_TYPE_ID": self.iblock_type_id,
    #         "IBLOCK_ID": self.iblock_id,
    #         "FIELDS": obj.dict(by_alias=True, exclude_none=True),
    #     }

    #     return self.client._request(method=method, params=params)

    # def update(self, obj):
    #     method = "lists.element.update.json"

    #     element_id = obj.id
    #     obj.id = None

    #     params = {
    #         "IBLOCK_TYPE_ID": self.iblock_type_id,
    #         "IBLOCK_ID": self.iblock_id,
    #         "ELEMENT_ID": element_id,
    #         "FIELDS": obj.dict(by_alias=True, exclude_none=True),
    #     }

    #     return self.client._request(method=method, params=params)

    def delete(self, element_id: int):
        method = "lists.element.delete.json"

        params = {
            "IBLOCK_TYPE_ID": self.iblock_type_id,
            "IBLOCK_ID": self.iblock_id,
            "ELEMENT_ID": element_id,
        }

        return self.client._request(method=method, params=params)
    
class ListClient(BaseListsClient):
    def __init__(self, client, iblock_id: int):
        super().__init__(
            client,
            pydantic_class=List,
            iblock_type_id="lists",
            iblock_id=iblock_id,
        )

class ListSocnetClient(BaseListsClient):
    def __init__(self, client, iblock_id: int):
        super().__init__(
            client,
            pydantic_class=ListSocnet,
            iblock_type_id="lists_socnet",
            iblock_id=iblock_id,
        )

class BitrixProcessClient(BaseListsClient):
    def __init__(self, client, iblock_id: int):
        super().__init__(
            client,
            pydantic_class=BitrixProcess,
            iblock_type_id="bitrix_processes",
            iblock_id=iblock_id,
        )