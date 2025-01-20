from django.urls import path
from . import views
urlpatterns=[
    path('sponserevent/<int:id>',views.sponserevents),
    path('sponserdec/<int:id>',views.sponserdec),

    path('mysponserships',views.mysponserships),
]