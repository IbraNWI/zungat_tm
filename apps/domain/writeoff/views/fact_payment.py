# views.py
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError

from apps.integrations.bx24.lib.schemas.crm.web_hooks.web_hook import WebhookSchema
from ..application.manual_writeoff import ManualWriteoffService



def parse_bitrix_payload(data: dict) -> dict:
    result = {}

    for key, value in data.items():
        value = value[0]

        match = re.match(r"(\w+)\[(.+)\]", key)

        if not match:
            result[key] = value
            continue

        root, child = match.groups()

        if root not in result:
            result[root] = {}

        result[root][child] = value

    return result


@csrf_exempt
def create_writeoff(request):
    try:
        payload = parse_bitrix_payload(
            dict(request.POST.lists())
        )

        webhook = WebhookSchema.model_validate(payload)['2']

        match = re.search(r'(\d+)$', webhook)
        result = match.group(1) if match else None   
        service = ManualWriteoffService().execute(fact_payment_id=int(result))


        return JsonResponse({
            "status": "success",
        })

    except ValidationError as e:
        print(e)

        return JsonResponse(
            {
                "status": "error",
                "errors": e.errors(),
            },
            status=400,
        )