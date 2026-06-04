import hashlib
import json
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from urllib3 import disable_warnings
from urllib3 import exceptions


from apps.integrations.tm_driver.lib.models.auth import TaxiMasterAuth
from apps.integrations.tm_driver.lib.services.driver_client import DriverClient
from apps.integrations.tm_driver.lib.services.operation_client import OperationClient

disable_warnings(exceptions.InsecureRequestWarning)


class LegacySSLAdapter(HTTPAdapter):
    
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.check_hostname = False
        ctx.verify_mode    = ssl.CERT_NONE
        ctx.minimum_version = ssl.TLSVersion.TLSv1
        ctx.set_ciphers("DEFAULT:@SECLEVEL=0")
        kwargs["ssl_context"] = ctx
        super().init_poolmanager(*args, **kwargs)

class TaxiMasterClient:

    API_VERSION = "1.0"
    API_NAME = "common_api"

    def __init__(self):
        self.auth = TaxiMasterAuth.objects.first()
        self._init_subclients()
        if not self.auth:
            raise Exception("Настройки TaxiMaster не найдены")
        self.base_url = f"{self.auth.host}/{self.API_NAME}/{self.API_VERSION}"
        self.session = requests.Session()
        self.session.mount("https://", LegacySSLAdapter())
    
    def _init_subclients(self):
        self.driver = DriverClient(self)
        self.operation = OperationClient(self)

    def _sign(self, params: dict) -> str:
        """Считаем подпись: MD5(строка_параметров + секретный_ключ)"""
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        raw = query_string + self.auth.secret_key
        return hashlib.md5(raw.encode()).hexdigest()
    
    def _sign_raw(self, body: str) -> str:
        raw = body + self.auth.secret_key
        return hashlib.md5(raw.encode("utf-8")).hexdigest()


    def get(self, method: str, params: dict = None) -> dict:
        params = params or {}
        signature = self._sign(params)
        response = self.session.get(
            url=f"{self.base_url}/{method}",
            params=params,
            headers={
                "Signature": signature,
                "X-User-Id": "3",
                "charset":"utf-8"
            },
            verify=False
        )
        return self._check_response(response)



    def post(self, method: str, data: dict = None, json_data: dict = None) -> dict:
        params = data or json_data or {}
        body = json.dumps(params)          # ← было urlencode, должно быть json.dumps
        signature = self._sign_raw(body)

        response = self.session.post(
            url=f"{self.base_url}/{method}",
            data=body,
            headers={
                "Content-Type": "application/json; charset=utf-8",  # ← было form-urlencoded
                "Signature": signature,
                "X-User-Id": "3",
            },
            verify=False
        )
        return self._check_response(response)

    def _check_response(self, response) -> dict:
        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"TaxiMaster ошибка {result.get('code')}: {result.get('descr')}")

        return result.get("data", {})