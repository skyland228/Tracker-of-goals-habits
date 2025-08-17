from django.http import HttpResponse


def Main(request):
    return HttpResponse("Главная страница")