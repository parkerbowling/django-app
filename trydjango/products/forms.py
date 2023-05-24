from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
    title = forms.CharField()
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"new-class-name two","rows":20,"cols":120}))
    price = forms.DecimalField(initial=199.99)
    
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price'
        ]
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not "CFE" in title:
            raise forms.ValidationError("This is not a valid title")
        return title
        
class RawProductForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"new-class-name two","rows":20,"cols":120}))
    price = forms.DecimalField(initial=199.99)