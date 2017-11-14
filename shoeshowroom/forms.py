from django import forms


class addprod(forms.Form):
	company=forms.CharField(required = True)
	modelname=forms.CharField(required = True)
	price=forms.IntegerField(required = True)
	outer_material=forms.CharField(required = True)
	neck_height=forms.CharField(required=True)
	occasion=forms.CharField(required = True)
	weight=forms.CharField(required = True)
	pack_of=forms.IntegerField(required = True)
	availability=forms.IntegerField(required = True)
	size=forms.IntegerField(required = True)

class addship(forms.Form):
	company=forms.CharField(required = True)
	phone=forms.CharField(required=True)
	email=forms.EmailField(required=True)