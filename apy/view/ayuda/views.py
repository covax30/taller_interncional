from django.shortcuts import render
def ayuda(request):
    return render(request, 'ayuda.html')