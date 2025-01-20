from django.urls import path
from . import views


urlpatterns=[
    path('',views.index),
    path('Login',views.doLogin),
    path('add_user/<int:ut>',views.add_user),
     path('logout',views.doLogout),
          path('about',views.about),

]