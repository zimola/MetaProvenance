from django.urls import path
from . import views

app_name = 'db'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('browse/', views.browse, name='browse'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('add/investigation/', views.add_investigations_view, name='add_investigation'),
    path('search/investigation/', views.investigation_search, name='search_investigation'),
    path('add/sample/', views.add_sample_view, name='add_sample'),
    path('add/wetlab/', views.add_wetlab_view, name='add_wetlab'),
    path('add/biological_protocol/', views.add_biological_protocol_view, name='add_biological_protocol'),
    path('add/pipeline_results/', views.add_pipeline_results_view, name='add_pipeline_results'),


]
