from django import forms
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext as _
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class FooterAdminForm(forms.ModelForm):
    class Meta:
        model = Footer
        fields = ('__all__')

    # ckeditor
    description = forms.CharField(widget=CKEditorUploadingWidget())


