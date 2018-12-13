from django.shortcuts import render, redirect
from .forms import UploadTestForm, CreateInvestigationForm, ConfirmSampleForm
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import JsonResponse

import django_tables2 as tables
from import_export import resources
from tablib import Dataset
import io
from django_ajax.decorators import ajax

from .formatters import format_sample_metadata, guess_filetype
from .models import Sample
import pandas as pd
import numpy as np


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

@login_required()
def confirm_samples_view(request):
    new_names = []
    form = None
    if 'confirm_samples' in request.session: 
        new_names = request.session['confirm_samples'].split(",")
        if request.method == 'POST':
            form = ConfirmSampleForm(new_names, request)
            if form.is_valid():
                print("SAVING")
                del request.session['confirm_samples']
                del request.session['confirm_visible']
                del request.session['confirm_type']
                return redirect('landing')
        else:
            #create an initial form
            form = ConfirmSampleForm(new_names)
    else:
        #Return some "nothing to confirm" screen?
        pass
    action = 'Confirm Samples'
    context = {'action': action,
               'form': form}
    return render(request, 'db/confirm_samples.html', context)


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

def search(request):
    return render(request, 'db/search.html', context={})


def browse(request):
    return render(request, 'db/browse.html', context={})

@login_required()
def upload_view(request):
    form = UploadTestForm(request.POST, request.FILES)
    if (request.method == 'POST') & form.is_valid():
        #If we've already been here, confirm_visible will be in the session
        #And that means a POST wants us to shuttle the upload data to a
        #confirmation page, depending on upload type
        if 'confirm_visible' in request.session:
            if 'confirm_type' not in request.session:
                #This shouldn't happen except for farked up sessions, but this
                #should jog the state back if it does
                del request.session['confirm_visible']
                del request.session['sample_names']
                return
            else:
                if request.session['confirm_type'] == 'sample_table':
                    return redirect("db:confirm_samples")
                else:
                    return redirect('landing')
        # File processing code
        # Guess what it is, then rewind the inmemoryfile
        guessed_type = guess_filetype(request.FILES['upload_file'])
        request.FILES['upload_file'].seek(0)
        
        if guessed_type == 'sample_table':
            table = format_sample_metadata(request.FILES['upload_file'])
            new_samples = []
            previously_registered = []
            for sample_id in np.unique(table['sample-id']):
                sc = Sample.objects.filter(name__exact=sample_id)
                if sc.count() > 0:
                    previously_registered.append(sample_id)
                else:
                    new_samples.append(sample_id)
            data = {'confirm_visible': True,
                    'confirm_type': guessed_type,
                    'num_new_samples': len(new_samples),
                    'num_registered_samples': len(previously_registered)}
            request.session['confirm_samples'] = ','.join(new_samples)
            request.session['confirm_visible'] = True
            request.session['confirm_type'] = guessed_type
            
        else:
            data = {'form': form, 'confirm_visible': False}
        return JsonResponse(data)
    else:
        data={'form': form, 'confirm_visible': False}
        return render(request, 'db/upload.html', data)
