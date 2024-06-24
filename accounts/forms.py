from django.contrib.auth.forms import UserCreationForm
from django import forms 
from .constants import GENDER_TYPE,ACCOUNT_TYPE
from django.contrib.auth.models import User
from .models import UserAddress,UserLibraryAccountModel

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username','password1','password2','first_name','last_name','email','birth_date','gender','account_type','street_address','city','postal_code','country']
    
    def save(self,commit=True):
        new_user = super().save(commit=False) 
        if commit==True:
            new_user.save()
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            account_type = self.cleaned_data.get('account_type')
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')

            UserAddress.objects.create(
                user=new_user,
                street_address=street_address,
                postal_code=postal_code,
                city=city,
                country=country
            )
            UserLibraryAccountModel.objects.create(
                user=new_user,
                account_type=account_type,
                gender=gender,
                birth_date = birth_date,
                account_number = 100000000 + new_user.id
            )
        return new_user
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'bg-gray-100 w-full text-sm px-4 py-3.5 rounded-md outline-blue-500'
                )
            })

class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name','last_name','email']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'bg-gray-100 w-full text-sm px-4 py-3.5 rounded-md outline-blue-500'
                )
            })
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserLibraryAccountModel.DoesNotExist:
                user_account = None
                user_address = None
            if user_account:
                self.fields['account_type'].initial = user_account.account_type
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date

                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country
                
        def save(self,commit=True):
            user = super().save(commit=False)
            if commit:
                user.save()
                user_account,created = UserLibraryAccountModel.objects.get_or_created(user=user)
                user_address,created = UserAddress.objects.get_or_created(user=user)

                user_account.account_type = self.cleaned_data['account_type']
                user_account.gender = self.cleaned_data['gender']
                user_account.birth_date = self.cleaned_data['birth_date']
                user_account.save()

                user_address.street_address = self.cleaned_data['street_address']
                user_address.city = self.cleaned_data['city']
                user_address.postal_code = self.cleaned_data['postal_code']
                user_address.country = self.cleaned_data['country']
                user_address.save()
            return user
