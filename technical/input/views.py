import json
from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewExcelImport, NewSelectForm
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
import time
import pandas as pd
from io import BytesIO
from .ingest import engine
from .models import Result


# I have no clue how frontend interaction works
# Create your views here.
def index(request):
    # TODO: I give up, I dont know how to handle front-end things.....
    select = NewSelectForm(request.GET)
    form = NewExcelImport(request.POST)
    if request.method == 'GET':
        if select.is_valid():
            response = [item['fields'] for item in json.loads(serializers.serialize("json", Result.objects.filter(epoch=select['Id'].value())))]
            return render(request, 'input/index.html', {'form': form, 'select': select, 'response': response})
    if request.method == 'POST':
        if form.is_valid():
            f = select.cleaned_data['file']
            print("hello world!")
    else:
        form = NewExcelImport()
        select = NewSelectForm()
    return render(request, 'input/index.html', {'form': form, 'select': select})


def result(request, id):
    r = Result.objects.get(epoch=id)
    return HttpResponse("<h1>Result:</h1><br><br><h2>%s</h2>" %(str(r)))


"""
After some research maybe the best approach would've been to rely on rest_framework
completely and use class based views along with its serializer to build the 
whole structure. However since im already here, I'll stick to this to avoid starting over...
Had I had more time I'd like to restructure it.
"""


@csrf_exempt
@api_view(('POST',))
# @renderer_classes((JSONRenderer,))
def insert_excel(request):
    epoch = round(time.time()*1000)
    f = request.FILES['file']
    try:
        df = pd.read_excel(BytesIO(f.read()))
        engine.insert_into_db(df, epoch)
    except Exception as err:  # TODO: Replace generic exception
        return Response({'status': "Error", "Description": str(err)})
    return Response({'status': "Success", "id": epoch})


@csrf_exempt
@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_data_from_epoch(request, id):
    return Response(item['fields'] for item in json.loads(serializers.serialize("json", Result.objects.filter(epoch=id))))
    # TODO: I dont like this one bit I NEED to refactor it
    # TODO: Maybe use rest_framework serializer instead?
