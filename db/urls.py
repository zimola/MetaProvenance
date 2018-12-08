from django.urls import path
from . import views

app_name = 'db'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('browse/', views.browse, name='browse'),
    path('upload/', views.UploadView.as_view(), name='upload'),
]
