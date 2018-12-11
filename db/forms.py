from django import forms
from django.db import models
from .models import Investigation


class UploadTestForm(forms.Form):

    is_selected = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    sample_metadata = models.FileField()


class CreateInvestigationForm(forms.ModelForm):

    class Meta:
        model = Investigation
        fields = '__all__'
