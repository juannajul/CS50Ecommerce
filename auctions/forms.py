from django import forms
from django.core import validators
from .models import Category, Auction, Bid

class FormCreateArticule(forms.Form):

    title = forms.CharField(label="Title", max_length=64, required=True, min_length=2, 
        widget = forms.TextInput(attrs={'placeholder': 'Insert Title', 'class': 'form-control'}),
        validators = [
            validators.MinLengthValidator(1, 'Insert a title')
        ] )      

    description = forms.CharField(label='Description', max_length=264, required=True, min_length=1,
        widget = forms.Textarea(attrs={'placeholder': 'Insert the description', 'class': 'form-control'}),
        validators = [
            validators.MinLengthValidator(1, 'Insert a description of your listing')
        ] )  

    bid_initial = forms.DecimalField(label="Initial Bid", max_digits=12, decimal_places=2, min_value=1,max_value=1000000)

    image_url = forms.URLField(label="Img Url", required=False, empty_value="https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png",
        widget = forms.URLInput(attrs={'placeholder': 'Insert img url', 'class': 'form-control'})
    )

    categories = Category.objects.all()
    options = []
    id_options = []
    name_options = []
    for cat in categories:
        id_category = cat.id
        name_category = cat.category
        option = [(cat.id, cat.category)]
        id_options.append(id_category)     
        name_options.append(name_category)  
        options.append(
            (id_category, name_category)
        )

    category = forms.TypedChoiceField(label="Category", choices=options, coerce=int)

class FormBid(forms.Form):
    new_bid = forms.DecimalField(label="", max_digits=12, decimal_places=2, min_value=1, max_value=1000000)

class FormComment(forms.Form):
    new_comment = forms.CharField(label="", max_length=264, required=True, 
        widget = forms.TextInput(attrs={'placeholder': 'Add Your Comment', 'class': 'form-control'}),
        validators = [
            validators.MinLengthValidator(1, 'Insert Your comment')
        ] )  
    
    
    
     