from django.urls import path

import ads.views as av

urlpatterns = [
    path('ads', av.index, name='ads'),
    path('ads/<int:pk>', av.index, name='ads_detail'),
]