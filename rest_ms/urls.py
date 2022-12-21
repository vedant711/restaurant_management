from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('delete', views.delete, name='delete'),
    path('feedback', views.feedback, name='feedback'),
    # path('ad', views.ad, name='ad'),
    path('bill', views.bill, name='bill'),

    path('deleteitems/<id>', views.deleteitems, name='deleteitems'),
    path('feedtable/<id>', views.feedtable, name='feedtable'),
    # path('adtable/<id>', views.adtable, name='adtable'),
    # path('billtable/<id>', views.billtable, name='billtable'),





    
]