from django.shortcuts import render

# Create your views here.
def index(request):
    pass
    return render(request, 'iteration2/index.html')

def test(request):
    pass
    return render(request, 'iteration2/test.html')