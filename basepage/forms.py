from django import forms
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext as _
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')

    # ckeditor
    description = forms.CharField(widget=CKEditorUploadingWidget())
    # multi choice files
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        label=_("Изображения"),
        required=False,
    )


    def clean_photos(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("images"):
            validate_image_file_extension(upload)

    def save_photos(self, product):
        """Process each uploaded image."""
        for upload in self.files.getlist("images"):
            image = ProductImage(product_id=product, image=upload)
            image.save()
