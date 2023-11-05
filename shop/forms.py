from django import forms


class ShippingForm(forms.Form):
    fullname = forms.CharField(label="Full name", max_length=100)
    address= forms.CharField(label="Address",max_length=200)
    city= forms.CharField(label="City",max_length=200)
    state= forms.CharField(label="State",max_length=200)
    zipcode= forms.CharField(label="Zip code",max_length=200)
