# views.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def echo(request):
    print("=" * 50)
    print("METHOD:", request.method)

    print("\nGET:")
    print(dict(request.GET))

    print("\nPOST:")
    print(dict(request.POST))

    print("\nBODY:")
    print(request.body.decode("utf-8"))

    try:
        body_json = json.loads(request.body)
        print("\nJSON:")
        print(json.dumps(body_json, indent=4, ensure_ascii=False))
    except Exception:
        pass

    print("=" * 50)

    return JsonResponse({"status": "ok"})