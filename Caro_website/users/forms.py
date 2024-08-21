from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import CustomUser, UserProfile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Отключить подсказки для всех полей формы
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.fields['username'].help_text = None
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            )
        )


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'shipping_address', 'full_name',  # 'shipping_last_name',
            # 'billing_first_name', 'billing_last_name', 'billing_address', 'payment'
        ]


class UserProfileForm(forms.ModelForm):
    # card_number = forms.CharField(
    #     required=False,
    #     max_length=19,
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Card Number',
    #         'autocomplete': 'off',
    #         'data-mask': '0000 0000 0000 0000'
    #     })
    # )
    # card_holder = forms.CharField(
    #     required=False,
    #     max_length=100,
    #     widget=forms.TextInput(attrs={
    #         'placeholder': 'Card Holder',
    #         'class': 'form-control text-uppercase',
    #         'autocomplete': 'off'
    #     })
    # )
    # expiration_date = forms.CharField(
    #     required=False,
    #     max_length=5,
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'MM/YY',
    #         'autocomplete': 'off',
    #         'data-mask': '00/00'
    #     })
    # )
    # cvv = forms.CharField(
    #     required=False,
    #     max_length=4,
    #     widget=forms.PasswordInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'CVV',
    #         'autocomplete': 'off',
    #         'data-mask': '0000'
    #     })
    # )

    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'shipping_address',  # 'shipping_last_name',
            # 'billing_first_name', 'billing_last_name', 'billing_address', 'payment'
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6 mb-0'),

            ),
            Row(
                Column('shipping_address', css_class='form-group col-md-12 mb-0'),
            ),
            # Row(
            #     Column('billing_first_name', css_class='form-group col-md-6 mb-0'),
            #     Column('billing_last_name', css_class='form-group col-md-6 mb-0'),
            #     css_class='form-row'
            # ),
            # Row(
            #     Column('billing_address', css_class='form-group col-md-12 mb-0'),
            # ),
            # Row(
            #     Column('card_number', css_class='form-group col-md-12 mb-0'),
            #     css_class='form-row'
            # ),
            # Row(
            #     Column('card_holder', css_class='form-group col-md-12 mb-0'),
            #     css_class='form-row'
            # ),
            # Row(
            #     Column('expiration_date', css_class='form-group col-md-6 mb-0'),
            #     Column('cvv', css_class='form-group col-md-6 mb-0'),
            #     css_class='form-row'
            # ),
            # Submit('submit', 'Save changes', css_class='btn btn-primary btn-block')
        )
