from django.shortcuts import render


def webapp(request):
    return render(request, "webapp/index.html")
