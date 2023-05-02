import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import FoodCategory,UserProfile,UserType,BusinessProfile,Rating,Food,Promotion

# Define your constants here
DIETARY_RESTRICTIONS = [
	('vegetarian', 'Vegetarian'),
	('halal', 'Halal'),
	('seafood_free', 'Seafood-Free'),
]
location_choices = [
	('', '---------'),
	('1', 'North'),
	('2', 'South'),
	('3', 'East'),
	('4', 'West'),
	('5', 'Central'),
]
GENDER_CHOICES = [
	('', 'Please Choose One'),
	('M', 'Male'),
	('F', 'Female'),
]

# Define your forms here
class FoodCategoryForm(forms.ModelForm):
	categoryName = forms.CharField(max_length=30)
	
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(FoodCategoryForm, self).__init__(*args, **kwargs)

	def save(self, commit=True, *args, **kwargs):
		instance = super(FoodCategoryForm, self).save(commit=False, *args, **kwargs)
		instance.categoryName = self.cleaned_data['categoryName']
		instance.adminID = self.request.user.id
		if commit:
			instance.save()
		return instance

	class Meta:
		model = FoodCategory
		fields = ["categoryName"]

class UserRegistrationForm(forms.Form):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	birthdate = forms.DateField()
	email = forms.EmailField()
	phone = forms.CharField(max_length=8)
	favorite_food = forms.CharField(max_length=30)
	preferred_location = forms.ChoiceField(choices=location_choices)
	food_category = forms.ModelChoiceField(queryset=FoodCategory.objects.all())
	dietary_restrictions = forms.MultipleChoiceField(choices=DIETARY_RESTRICTIONS, widget=forms.CheckboxSelectMultiple())
	username = forms.CharField(max_length=30)
	password = forms.CharField(widget=forms.PasswordInput)
	gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Gender')

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		self.user_profile = kwargs.pop('user_profile', None)
		super(UserRegistrationForm, self).__init__(*args, **kwargs)

	def clean_preferred_location(self):
		preferred_location = self.cleaned_data.get('preferred_location')
		if not preferred_location:
			raise forms.ValidationError("Please select a valid location.")
		return preferred_location

	def clean_gender(self):
		gender = self.cleaned_data.get('gender')
		if not gender:
			raise forms.ValidationError("Please select a valid gender.")
		return gender

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		if not re.match(r'^\d{8}$', phone):
			raise forms.ValidationError("Please enter a valid phone number")
		return phone

	# Override the default save method to save to UserProfile and UserType models
	def save(self, commit=True):
		user = User.objects.create_user(
			username=self.cleaned_data['username'],
			password=self.cleaned_data['password'],
			email=self.cleaned_data['email'],
			first_name=self.cleaned_data['first_name'],
			last_name=self.cleaned_data['last_name']
		)

		user_profile = UserProfile.objects.create(
			user=user,
			birthdate=self.cleaned_data['birthdate'],
			phone=self.cleaned_data['phone'],
			favFood=self.cleaned_data['favorite_food'],
			prefLocation=self.cleaned_data['preferred_location'],
			foodCategory=self.cleaned_data['food_category'],
			gender=self.cleaned_data['gender'],
			dietary_restrictions=self.cleaned_data['dietary_restrictions'],
		)

		user_type = UserType.objects.create(
			user=user,
			userType='user'
		)

		return (user, user_profile, user_type)

class UserUpdateForm(UserRegistrationForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Leave this field empty if you don't want to change the password.",
    )

class BusinessRegistrationForm(forms.Form):
	company_name = forms.CharField(max_length=50)
	uen = forms.CharField(max_length=10)
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	email = forms.EmailField()
	phone = forms.CharField(max_length=8)
	address = forms.CharField(max_length=100)
	postal_code = forms.CharField(max_length=6)
	food_category = forms.ModelChoiceField(queryset=FoodCategory.objects.all())
	username = forms.CharField(max_length=30)
	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		self.business_profile = kwargs.pop('business_profile', None)
		super(BusinessRegistrationForm, self).__init__(*args, **kwargs)

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		if not re.match(r'^\d{8}$', phone):
			raise forms.ValidationError("Please enter a valid phone number")
		return phone

	# Override the default save method to save to BusinessProfile and UserType models
	def save(self, commit=True):
		user = User.objects.create_user(
			username=self.cleaned_data['username'],
			password=self.cleaned_data['password'],
			email=self.cleaned_data['email'],
			first_name=self.cleaned_data['first_name'],
			last_name=self.cleaned_data['last_name']
		)

		business_profile = BusinessProfile.objects.create(
			user=user,
			companyName=self.cleaned_data['company_name'],
			uen=self.cleaned_data['uen'],
			phone=self.cleaned_data['phone'],
			address=self.cleaned_data['address'],
			postalCode=self.cleaned_data['postal_code'],
			foodCategory=self.cleaned_data['food_category']
		)

		user_type = UserType.objects.create(
			user=user,
			userType='business'
		)

		return (user, business_profile, user_type)

class BusinessUpdateForm(BusinessRegistrationForm):
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		required=False,
		help_text="Leave this field empty if you don't want to change the password.",
	)
	class Meta:
		model = BusinessProfile
		exclude = ['uen']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['user', 'food', 'rating']

class FoodForm(forms.ModelForm):
	dietary_restrictions = forms.MultipleChoiceField(choices=DIETARY_RESTRICTIONS, widget=forms.CheckboxSelectMultiple())

	class Meta:
		model = Food
		fields = ['foodName', 'foodCategory', 'dietary_restrictions']

	def save(self, commit=True):
		instance = super().save(commit=False)
		dietary_restrictions = self.cleaned_data.get('dietary_restrictions')
		instance.dietary_restrictions = ','.join(dietary_restrictions) if dietary_restrictions else None
		if commit:
			instance.save()
		return instance

class PromotionForm(forms.ModelForm):
	class Meta:
		model = Promotion
		fields = ['title', 'description', 'startDate', 'endDate']

	def clean(self):
		cleaned_data = super().clean()
		start_date = cleaned_data.get('startDate')
		end_date = cleaned_data.get('endDate')

		if start_date and end_date and end_date < start_date:
			self.add_error('endDate', 'End date should be later than start date.')
			# raise forms.ValidationError('End date should be later than start date.')
		return cleaned_data

