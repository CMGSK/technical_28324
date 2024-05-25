from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from import_export.results import Result
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
import time
import pandas as pd
from io import BytesIO
import ingest.engine as ingest


@csrf_exempt
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def insert_excel(request):
    epoch = round(time.time()*1000)
    try:
        if request.method != "POST":
            raise Exception("Unallowed method")
        f = request.FILES['file']
        df = pd.read_excel(BytesIO(f.read()))
        if ingest.insert_into_db(df, epoch):
            return Response({'status': "Success", "id": epoch})
    except Exception as err:
        return Response({"status": str(err)})


@csrf_exempt
@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_data(request, id):
    serial = serializers.serialize("json", Result.objects.filter(epoch=id).all())
    return Response(serial)