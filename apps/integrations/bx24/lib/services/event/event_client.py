from apps.integrations.bx24.lib.schemas.events.event import Event
class EventClient:
    def __init__(
            self,
            client
            ):
        self.client = client
        self.pydantic_class = Event
        self.endpoint = "event"
    
    def bind(self,event,handler):
        method = f"{self.endpoint}.bind"
        params = {
            "event":event,
            "handler":handler
            }
        response = self.client._request(method=method,params=params)["result"]
        return response
    
    def unbind(self,event,handler):
        method = f"{self.endpoint}.unbind"
        params = {
            "event":event,
            "handler":handler
            }
        response = self.client._request(method=method,params=params)["result"]
        entity = self.pydantic_class(**response)
        return entity
    
    def get(self):
        method = f"{self.endpoint}.get"
        params = {}
        response = self.client._request(method=method,params=params)
        if response is None:
            return []
        else:
            response = response["result"]
        entities = [self.pydantic_class(**item) for item in response]
        return entities
    
    def events(self,scope=None,full:bool=False):
        method = f"events"
        params = {}
        if scope is None:
            params["SCOPE"] = scope
        if full == True:
            params["FULL"] = full
        response = self.client._request(method=method,params=params)["result"]
        return response
