from .base_model import BaseConfigModel

class AuthSchema(BaseConfigModel):
    domain: str
    client_endpoint: str
    server_endpoint: str
    member_id: str


class DocumentIdSchema(BaseConfigModel):
    _0: str
    _1: str
    _2: str


class WebhookSchema(BaseConfigModel):
    document_id: dict
    auth: AuthSchema