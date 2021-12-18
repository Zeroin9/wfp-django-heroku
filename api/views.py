import json
from datetime import datetime
from django.core import serializers
from django.http import JsonResponse
from django.utils.timezone import get_current_timezone
from .models import Parcel, Operation, Token, ParcelTokenLink
from .authentification_utils import generate_new_token, auth_need
from .tracking_utils import get_opers

# Create new parcel
@auth_need
def for_parcel(request):
    token = str(request.headers.get('AuthToken'))
    token_instance = Token.objects.filter(token=token)[0]
    if request.method == "GET": # get method
        parcel_pk = request.GET.get("pk")
        if parcel_pk is None: # Get all
            parcels = []
            parcelsWithTokens = ParcelTokenLink.objects.filter(token=token_instance)
            for p in parcelsWithTokens:
                parcels.append(serialize_instance(p.parcel))
            return JsonResponse({'parcels':parcels}, status=200)
        else: # get with this pk
            try:
                parcel = Parcel.objects.get(id=int(parcel_pk))
            except Exception:
                return JsonResponse({'error':"not foun with such 'pk'"}, status=404)
            return JsonResponse(serialize_instance(parcel), status=200)
    if request.method == "POST": # create new
        parcel_code = request.GET.get("code")
        if (parcel_code is None or parcel_code == ""):
            return JsonResponse({'error':"'code' is required "}, status=400)
        try:
            parcel_instance = Parcel.objects.filter(track_code=parcel_code)[0]
            same = ParcelTokenLink.objects.filter(token=token_instance, parcel=parcel_instance).count()
            if same == 0:
                ParcelTokenLink.objects.create(parcel=parcel_instance, token=token_instance)
        except Exception:
            parcel_instance = Parcel.objects.create(track_code=parcel_code)
            ParcelTokenLink.objects.create(parcel=parcel_instance, token=token_instance)
        return JsonResponse({'new_parcel':serialize_instance(parcel_instance)}, status=201)

# Get all operations for parcel by 'pk'
def get_oper_by_parcel(request):
    if request.method == "GET":
        parcel_pk = request.GET.get("parcel_pk")
        if (parcel_pk is None):
            return JsonResponse({'error':"'parcel_pk' is required"}, status=400)
        try:
            parcel = Parcel.objects.get(id=int(parcel_pk))
        except Exception:
            return JsonResponse({'error':"not foun with such 'pk'"}, status=404)
        opers = []
        operObjects = Operation.objects.filter(parcel=parcel)
        for o in operObjects:
            opers.append(serialize_instance(o))
        return JsonResponse({'parcel':serialize_instance(parcel), 'operations':opers})
    if request.method == "POST":
        return JsonResponse({'error':'Only GET here'}, status=400)

# Refresh operations for parcel by 'pk'
def update_oper_by_parcel(request):
    if request.method == "GET":
        return JsonResponse({'error':'Only GET here'}, status=400)
    if request.method == "POST":
        parcel_pk = request.GET.get("parcel_pk")
        if (parcel_pk is None):
            return JsonResponse({'error':"'parcel_pk' is required"}, status=400)
        try:
            parcel = Parcel.objects.get(id=int(parcel_pk))
        except Exception:
            return JsonResponse({'error':"not foun with such 'pk'"}, status=404)
        opers_data = get_opers(parcel.track_code)
        if opers_data is None:
            return JsonResponse({'error':"tracking.pochta.ru API problem"}, status=503)
        Operation.objects.filter(parcel=parcel).delete()
        parcel.updated_date = datetime.now(tz=get_current_timezone())
        for oper_data in opers_data:
            Operation.objects.create(
                date=oper_data['date'],
                postOfficeIndex=oper_data['index'],
                postOfficeName=oper_data['post_office'],
                name=oper_data['oper_name'],
                parcel=parcel
            )
        operObjects = Operation.objects.filter(parcel=parcel)
        opers = []
        for o in operObjects:
            opers.append(serialize_instance(o))
        return JsonResponse({'parcel':serialize_instance(parcel), 'operations':opers})

# Get new auth token
def get_new_token(request):
    if request.method == "GET":
        return JsonResponse({'error':'Only POST here'}, status=400)
    if request.method == "POST":
        token = request.headers.get('AuthToken')
        if token is None:
            new_token = generate_new_token()
            return JsonResponse({'token':new_token}, status=201)
        else:
            return JsonResponse({'error':'You have already send token'}, status=400)

def serialize_instance(instance):
    data = serializers.serialize('json', [instance])
    struct = json.loads(data)[0]
    return struct