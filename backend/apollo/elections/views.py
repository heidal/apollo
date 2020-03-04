from django.http import HttpResponse


def index(request):
    return HttpResponse("Elections index response")
