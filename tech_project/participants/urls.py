from django.urls import path
from . import views
urlpatterns=[
        path('addfeedback',views.addfeedback),
        path('viewfeedback',views.viewfeedback),
        path('addmembers/<int:id>',views.addmembers),
        path('view_members/<int:id>',views.view_members),
        path('myregistrations',views.myregistrations),
        path('viewcertificates',views.viewcertificates),
        path('Registerevent/<int:id>',views.Registerevent),
        path('cancelevent/<int:id>',views.cancelevent),
    path('deletemyaccount',views.deletemyaccount),





]