from django import forms
from members.models import Produk

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ProductForm(BaseForm):
	class Meta:
		model = Produk
		fields = "__all__"
