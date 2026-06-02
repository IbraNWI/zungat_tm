from django.http import JsonResponse



def writeoff_func(request):
    if request.method == "GET":
        data = {"message": "ok", "query": request.GET.dict()}
        return JsonResponse(data)