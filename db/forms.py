from django import forms
from django.db import models
from .models import Investigation, Sample


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
