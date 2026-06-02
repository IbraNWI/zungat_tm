from apps.integrations.tm_driver.lib.schemas.operation import Operation


class OperationClient():
    
    def __init__(self, client):
        self.client = client
        self.pydantic_class = Operation
    
    def get(self,id,start_time,finish_time):
        method = "get_driver_operations"
        params = {
            "driver_id":id,
            "start_time":start_time,
            "finish_time":finish_time
            }
        response = self.client.get(method=method,params=params)
        entity = self.pydantic_class(**response)
        return entity
    
    def add(self,operation:Operation):
        method = "create_driver_operation"
        data = operation.dict(by_alias=True,exclude_none=True)
        response = self.client.post(method=method,json=data)
        entity = self.pydantic_class(**response)
        return entity

    def cencel(self):
        ...