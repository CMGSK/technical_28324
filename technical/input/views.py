from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewExcelImport


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = NewExcelImport(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = NewExcelImport()
    return render(request, 'input/index.html', {'form': form})


def result(request, id):
    # r = Result.objects.get(epoch=id)
    return HttpResponse("<h1>Result:</h1><br><br><h2>%s</h2>" %(str(r)))
