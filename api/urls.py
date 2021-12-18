from django.urls import path

from . import views

urlpatterns = [
    path('operations', views.get_oper_by_parcel, name='operations'), #GET only
    path('new_token', views.get_new_token, name='new_token'), #POST only
    path('parcel', views.for_parcel, name='parcel'), #GET and POST
    path('refresh', views.update_oper_by_parcel, name='refresh'), #POST only
]