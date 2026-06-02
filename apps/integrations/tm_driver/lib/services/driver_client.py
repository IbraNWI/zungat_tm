from apps.integrations.tm_driver.lib.schemas.driver import Driver

class DriverClient():
    def __init__(self, client):
        self.client = client
        self.pydantic_class = Driver
    


    def get(self,id):
        method = "get_driver_info"
        params = {
            "driver_id":id
            }
        response = self.client.get(method=method,params=params)
        entity = self.pydantic_class(**response)
        return entity
    
    def add(self,driver:Driver):
        method = "create_driver"
        data = driver.dict(by_alias=True,exclude_none=True)
        response = self.client.post(method=method,json=data)
        entity = self.pydantic_class(**response)
        return entity
    
    def update(self):
        method = "update_driver_info"
        return None
    
    def delete(self):
        return None

    def list(self,locked_drivers=False,dismissed_drivers=False,fields=""):
        method = "get_drivers_info"
        params = {
            "locked_drivers":locked_drivers,
            "dismissed_drivers":dismissed_drivers,
            "fields":fields
            }
        response = self.client.get(method=method,params=params)
        entities = [self.pydantic_class(**i) for i in response]
        return entities