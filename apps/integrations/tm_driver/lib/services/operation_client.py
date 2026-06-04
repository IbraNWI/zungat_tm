from apps.integrations.tm_driver.lib.schemas.operation import Operation


class OperationClient():
    
    def __init__(self, client):
        self.client = client
        self.pydantic_class = Operation
    
    def get(self,driver_id,start_time,finish_time):
        start_time = start_time.strftime("%Y%m%d%H%M%S")
        finish_time = finish_time.strftime("%Y%m%d%H%M%S")
        method = "get_driver_operations"
        params = {
            "driver_id":driver_id,
            "start_time":start_time,
            "finish_time":finish_time
            }
        response = self.client.get(method=method,params=params)
        if response is None:
            return []
        else:
            entities = [self.pydantic_class(**entity) for entity in response["operations"]]
            return entities

    
    def add(self,operation:Operation):
        method = "create_driver_operation"
        data = operation.dict(by_alias=True,exclude_none=True)
        response = self.client.post(method=method,data=data)
        entity = self.pydantic_class(**response)
        return entity

    def cencel(self):
        ...