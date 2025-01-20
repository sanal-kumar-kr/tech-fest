from django.urls import path
from . import views
urlpatterns=[
     path('users',views.users),
    path('add_event',views.add_event),
    path('view_events',views.View_events),
    path('editevent/<int:id>',views.editevent),
    path('deleteevent/<int:id>',views.deleteevent),
    path('updateprice/<int:id>',views.updateprice),
    path('approve_user/<int:id>',views.approve_user),
    path('reject_user/<int:id>',views.reject_user),
    path('enable_user/<int:id>',views.enable_user),
    path('disable_user/<int:id>',views.disable_user),
    path('generatecertificates/<int:id>',views.generatecertificates),
    path('view_users/<int:ut>',views.view_users),
    path('userreq',views.usersreq),
    path('viewregistrations/<int:id>',views.registrations),
    path('addecorations',views.addecorations),
    path('viewdecorations',views.viewdecorations),
    path('userreq',views.usersreq),
    path('edit_dec/<int:id>',views.edit_dec),
    path('delete_dec/<int:id>',views.delete_dec),


    
    
]