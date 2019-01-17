"""metaprovenance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from landingpage.views import index
from db.views_ajax import InvestigationGridView, ReplicateFkWidgetGrid, SampleFkWidgetGrid
from db.views import (
InvestigationCreate, InvestigationDetail, InvestigationList, InvestigationUpdate
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('', index, name='landing'),
    re_path(r'db/investigation/all/$', InvestigationList.as_view(), 
            name='investigation_all',
            kwargs={'view_title': 'All Investigations', 'allow_anonymous': True}),
    re_path(r'db/investigation/create/$', InvestigationCreate.as_view(),
        name='investigation_create',
        kwargs={'view_title': "Create New Investigation", 'allow_anonymous': False}),
    re_path(r'db/investigation/(?P<investigation_id>\d+)/$', InvestigationDetail.as_view(),
        name='investigation_detail',
        kwargs={'view_title': 'All Investigations', 'allow_anonymous': True}),
    re_path(r'db/investigation/edit/(?P<investigation_id>\d+)/$', InvestigationUpdate.as_view(),
        name='investigation_update',
        kwargs={'view_title': 'Update Investigation', 'allow_anonymouys': False}),
    re_path(r'db/sample-grid(?P<action>/?\w*)/$', SampleFkWidgetGrid.as_view(),
        name='sample_grid', kwargs={'ajax':True}),
    re_path(r'db/replicate-grid(?P<action>/?\w*)/$', ReplicateFkWidgetGrid.as_view(),
        name='replicate_grid', kwargs={'ajax':True})
#    re_path(r'db/investigation/all(?P<action>/?\w*)/$', InvestigationGridView.as_view(),
#            name='investigation_all',
#            kwargs={'view_title': 'Simple investigation grid'}),
#    url('db/', include('db.urls')),
]

js_info_dict = {
            'domain': 'djangojs',
            'packages': ('metaprovenance',),
                }

try:
    from django.views.i18n import JavaScriptCatalog
    urlpatterns += [
        url(r'^jsi18n/$', JavaScriptCatalog.as_view(**js_info_dict), name='javascript-catalog'),
    ]
except ImportError:
    from django.views.i18n import javascript_catalog
    urlpatterns += [
        url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog',)
    ]
