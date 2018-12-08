from django.shortcuts import render
from .forms import UploadTestForm
from django.http import JsonResponse
from django.views import View

import django_tables2 as tables

from .formatters import format_sample_metadata

import pandas as pd

class SampleNameTable(tables.Table):
    selected = tables.columns.CheckBoxColumn(orderable=False,
                                             checked="is_selected")
    name = tables.Column()

class MetadataKeyTable(tables.Table):
    key = tables.Column()

def search(request):
    return render(request, 'db/search.html', context={})


def browse(request):
    return render(request, 'db/browse.html', context={})


class UploadView(View):
    def get(self, request):
        print("Session keys:")
        for var in request.session.keys():
            print(var)
        print("GET keys:")
        for var in request.GET.keys():
            print(var)
        data={}
        if request.session.get('sample_table'):
            data['sample_table'] = request.session['sample_table']
        return render(request, 'db/upload.html', data)

    def post(self, request):
        form = UploadTestForm(request.POST, request.FILES)
        if form.is_valid():
            table = format_sample_metadata(request.FILES['file'])
            print(table)
            data = {'is_valid': True}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
