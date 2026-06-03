# views.py


from pprint import pprint

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError

from .hook_parser import parse_bitrix_payload
from apps.integrations.bx24.lib.schemas.crm.web_hooks.web_hook import WebhookSchema


@csrf_exempt
def create_writeoff(request):
    try:
        payload = parse_bitrix_payload(
            dict(request.POST.lists())
        )

        webhook = WebhookSchema.model_validate(payload)

        print("=" * 50)
        print("BITRIX WEBHOOK")
        pprint(webhook.model_dump())
        print("=" * 50)

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