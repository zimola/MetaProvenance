from django.shortcuts import render, redirect
from .forms import UploadTestForm, CreateInvestigationForm
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required

#from .models import Investigation

import django_tables2 as tables

from .formatters import format_sample_metadata

#import pandas as pd


'''
INVESTIGATIONS
'''


@login_required()
def add_investigations_view(request):
    form = CreateInvestigationForm(request.POST or None)
    action = "Create Investigation"
    if request.method == 'POST' and form.is_valid:
        # todo handle is investigation exists. -> Create or search:
        investigation = form.save()
        request.session['investigation_name'] = investigation.name
        return redirect('landing')
    context = {'form': form, 'action': action}
    return render(request, 'db/add_investigation.html', context)


def investigation_search(request):
    # todo full text search on investigation table
    query = request.GET.get('q')
    print(query)
    return redirect('db:add_investigation')

def list_of_investigations():
    #todo, list of 20 or so most recent investigations
    pass


'''
SAMPLES
'''


@login_required()
def add_sample_view(request):
    # todo make html
    action = 'Add Samples'
    context = {'action': action}
    return render(request, 'db/add_sample.html', context)


'''
WETLAB
'''


@login_required()
def add_wetlab_view(request):
    # todo make html
    action = 'Add Wetlab Data'
    context = {'action': action}
    return render(request, 'db/add_wetlab.html', context)


'''
BIOLOGICAL PROTOCOL
'''


@login_required()
def add_biological_protocol_view(request):
    #  todo make html
    action = 'Add Biological Protocol Data'
    context = {'action': action}
    return render(request, 'db/add_biological_protocol.html', context)


'''
PIPELINERESULTS
'''


def add_pipeline_results_view(request):
    # todo make html
    action = 'Add Pipeline Results'
    context = {'action': action}
    return render(request, 'db/add_pipeline_results.html', context)


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
