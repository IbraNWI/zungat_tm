import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def echo(request):
    if request.method == "GET":
        return HttpResponse(request.GET.urlencode() or "{}", content_type="text/plain")

    if request.method == "POST":
        body = request.body.decode("utf-8") or ""
        # если JSON — вернуть как JSON, иначе как текст
        try:
            data = json.loads(body) if body else {}
            print(data)
            return JsonResponse(data)
        except json.JSONDecodeError:
            return HttpResponse(body, content_type="text/plain")

    return HttpResponse(status=405)