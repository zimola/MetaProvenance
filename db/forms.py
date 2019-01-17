from django import forms
from django.db import models
from .models import BiologicalReplicate, Investigation, Sample

from django_jinja_knockout.forms import (
    DisplayModelMetaclass, FormWithInlineFormsets, RendererModelForm,
    ko_inlineformset_factory
)

'''
Django-Jinja-Knockout Forms
'''

class InvestigationForm(RendererModelForm):
    class Meta(RendererModelForm.Meta):
        model = Investigation
        fields = '__all__'

class InvestigationDisplayForm(RendererModelForm, 
                               metaclass=DisplayModelMetaclass):
    class Meta(InvestigationForm.Meta):
        pass

class SampleForm(RendererModelForm):
    class Meta:
        model = Sample
        fields = '__all__'

class SampleDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = Sample
        fields = '__all__'

class ReplicateForm(RendererModelForm):
    class Meta:
        model = BiologicalReplicate
        fields = '__all__'

class ReplicateDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = BiologicalReplicate
        fields = '__all__'

InvestigationSampleFormset = ko_inlineformset_factory(Investigation,
                                                      Sample,
                                                      form=SampleForm,
                                                      extra=0,
                                                      min_num=0)
InvestigationDisplaySampleFormset = ko_inlineformset_factory(
                                                 Investigation,
                                                 Sample,
                                                 form=SampleDisplayForm)
InvestigationReplicateFormset = ko_inlineformset_factory(Investigation,
                                                         BiologicalReplicate,
                                                         form=ReplicateForm,
                                                         extra=0)
InvestigationDisplayReplicateFormset = ko_inlineformset_factory(
                                                 Investigation,
                                                 BiologicalReplicate,
                                                 form=ReplicateDisplayForm)

class InvestigationWithInlineFormsets(FormWithInlineFormsets):
    FormClass = InvestigationForm
    FormsetClasses = [InvestigationSampleFormset,
                      InvestigationReplicateFormset]

class InvestigationWithInlineSamples(FormWithInlineFormsets):
    FormClass = InvestigationForm
    FormsetClasses = [InvestigationSampleFormset]

    def get_bs_form_opts(self):
        return {
            'class': 'investigation',
            'title': format_html('Edit "{}"', self.object),
            'submit_text': 'Save Investigation'
        }

class InvestigationDisplayWithInlineFormsets(FormWithInlineFormsets):
     FormClass = InvestigationDisplayForm
     FormsetClasses = [InvestigationDisplaySampleFormset,
                       InvestigationDisplayReplicateFormset]

''' Django Forms '''

class UploadTestForm(forms.Form):
    upload_file = models.FileField() 

class CreateInvestigationForm(forms.ModelForm):
    class Meta:
        model = Investigation
        fields = '__all__'

class ConfirmSampleForm(forms.Form):
    """ A manually generated form that outputs BooleanFields for
    each new sample that is being added, and asks the user to confirm that
    they wish them to be added """
    def __init__(self, new_samples, request=None,
                       *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for i in range(len(new_samples)):
            field_name = 'new_sample_%d' % (i,)
            self.fields[field_name] = forms.BooleanField(label=new_samples[i], required=False)
            self.initial[field_name] = True

    def clean(self):
        samples = set()
        i = 0
        field_name = 'new_sample_%d' % (i,)
        while self.cleaned_data.get(field_name):
           sample = self.cleaned_data[field_name]
           samples.add(sample)
           i += 1
           field_name = 'new_sample_%d' % (i,)
        self.cleaned_data["samples"] = samples

    def save(self):
        #TODO: get investigation and assign it properly here
        vsi = self.instance
        vsi.new_sample_set.all().delete()
        for sample in self.cleaned_data["samples"]:
           Sample.objects.create(name=sample, investigation=0)

    def get_sample_checklist(self):
        for field_name in self.fields:
            if field_name.startswith('new_sample_'):
                yield self[field_name]
