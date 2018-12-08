from django import forms
from django.db import models

class UploadTestForm(forms.Form):
    is_selected = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    sample_metadata = models.FileField()
