# views.py
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError
from ..application.manual_writeoff import ManualWriteoffApplication



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
def accept_writeoff(request):
    try:
        payload = parse_bitrix_payload(
            dict(request.POST.lists())
        )

        match = re.search(r'(\d+)$', payload["document_id"]["2"])
        result = match.group(1) if match else None   
        service = ManualWriteoffApplication().execute(fact_payment_id=int(result))


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