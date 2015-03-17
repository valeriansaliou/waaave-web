from django import forms
from django_countries.data import COUNTRIES as list_countries
from _commons.forms import defaults
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from _commons.shortcuts import get_user
from _commons.validators import _is_valid
from _commons.forms.errors import field_error

from .models import *


# -- Helper: check if passwords match
def _clean_password_confirm(self, first_input='password', second_input='password_confirm'):
    password = self.cleaned_data.get(first_input)
    password_confirm = self.cleaned_data.get(second_input)

    if not password_confirm:
        raise forms.ValidationError('Please confirm your password (enter it again).', 'required')
    if password_confirm != password:
        raise forms.ValidationError('Passwords do not match', 'invalid')

    return password_confirm


# -- Helper: check if email is acceptable
def _clean_email(self, field='email'):
    """
    Clean an email in a form field
    """
    value = self.cleaned_data.get(field)
    user = User.objects.filter(email=value)

    if user.count()\
       and (not hasattr(self, 'uid') or (not self.uid in [u.id for u in user])):
        error_message = "This email is already taken."

        if field and self.fields:
            field_error(self, field, error_message)
        else:
            raise ValidationError(error_message, 'taken')

    return value


# -- Helper: clean all values
def _clean_entitle(self, field):
    """
    Clean a form field value
    """
    value = self.cleaned_data.get(field)

    if value:
        value = value.title().strip()

    return value


# -- Helper: validate after stripping value
def _validate_strip(value):
    if not value or not value.strip():
        raise ValidationError(None, 'required')


# -- Login: Root
class LoginRootForm(forms.Form):
    """
    Account > Login Root Form
    """

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
        attrs={
            'class': 'email',
            'placeholder': 'Type your email',
            'pattern': defaults.PATTERN_USERNAME

        })
    )

    password = forms.CharField(
        required=True,
        min_length=defaults.PWD_LENGTH_MIN,
        max_length=defaults.PWD_LENGTH_MAX,
        widget=forms.PasswordInput(
        attrs={
            'class': 'password',
            'placeholder': 'Enter your password',
            'pattern': defaults.PATTERN_PWD
        })
    )

    remember = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(attrs={ 'id': 'rememberMe', 'class': 'checkbox-slide'})
    )

    def is_valid(self):
        return _is_valid(self, forms.Form)


# -- Register: Step 1 (go)
class RegisterGoForm(forms.Form):
    """
    Account > Register Go Form
    """
    def __init__(self, *args, **kwargs):
        self.has_password = kwargs.pop('has_password') if 'has_password' in kwargs else True
        super(forms.Form, self).__init__(*args, **kwargs)

        self.fields['email'] = forms.EmailField(
            required=True,

            widget=forms.TextInput(
                attrs={
                    'type': 'email',
                    'class': 'email',
                    'placeholder': 'Your Email Address',
                    'pattern': defaults.PATTERN_EMAIL
                }
            ),

            error_messages={
                'required': 'Please enter your email address.',
                'invalid': 'Enter a valid email address.'
            }
        )

        if self.has_password:
            print("HAS PASSWORD")
        else:
            print("HAS NO PASSWORD")

        if self.has_password:
            self.fields['password'] = forms.CharField(
                required=True,
                min_length=defaults.PWD_LENGTH_MIN,
                max_length=defaults.PWD_LENGTH_MAX,

                widget=forms.PasswordInput(
                    attrs={
                        'class': 'password',
                        'placeholder': 'Your Password',
                        'pattern': defaults.PATTERN_PWD,
                        'data-equal': 'password_confirm',
                        'data-equal-redirect': '1'
                    }
                ),

                error_messages={
                    'required': 'Please enter your password.',
                    'invalid': 'Password too short (' + str(defaults.PWD_LENGTH_MIN) + ' to ' + str(defaults.PWD_LENGTH_MAX) + ' chars).'
                }
            )

            self.fields['password_confirm'] = forms.CharField(
                required=True,
                min_length=defaults.PWD_LENGTH_MIN,
                max_length=defaults.PWD_LENGTH_MAX,

                widget=forms.PasswordInput(
                    attrs={
                        'class': 'password-confirm',
                        'placeholder': 'Confirm your Password',
                        'pattern': defaults.PATTERN_PWD,
                        'data-equal': 'password'
                    }
                ),

                error_messages={
                    'required': 'Please confirm your password (enter it again).',
                    'invalid': 'Passwords do not match'
                }
            )

        self.fields['terms_agree'] = forms.BooleanField(
            initial=True,

            widget=forms.CheckboxInput(
                attrs={
                    'id': 'termsCb',
                    'class': 'checkbox-classic'
                }
            ),

            error_messages={
                'required': 'Please agree to our terms.'
            }
        )

    def clean_password_confirm(self):
        if self.has_password:
            return _clean_password_confirm(self)

    def clean_email(self):
        return _clean_email(self)

    def is_valid(self):
        return _is_valid(self, forms.Form)


# -- Register: Step 2 (profile)
class RegisterProfileForm(forms.Form):
    """
    Account > Register Profile Form
    """
    first_name = forms.CharField(
        required=True,
        validators=[_validate_strip],
        max_length=defaults.DEFAULT_MAX,

        widget=forms.TextInput(
            attrs={
                'class': 'first-name',
                'placeholder': 'Your First Name'
            }
        ),

        error_messages={
            'required': 'Enter your first name, please.',
            'invalid': 'Your first name looks invalid.'
        }
    )

    last_name = forms.CharField(
        required=True,
        validators=[_validate_strip],
        max_length=defaults.DEFAULT_MAX,

        widget=forms.TextInput(
            attrs={
                'class': 'last-name',
                'placeholder': 'Your Last Name'
            }
        ),

        error_messages={
            'required': 'Enter your last name, please.',
            'invalid': 'Your last name looks invalid.'
        }
    )

    city = forms.CharField(
        required=True,
        validators=[_validate_strip],
        max_length=defaults.DEFAULT_MAX,

        widget=forms.TextInput(
            attrs={
                'class': 'city',
                'placeholder': 'Your City'
            }
        ),

        error_messages={
            'required': 'We need your city to put you in touch with near developers.',
            'invalid': 'Your city looks invalid.'
        }
    )

    country = forms.ChoiceField(
        required=True,
        choices=(
            [('', 'Select your Country.')] + 
            sorted(
                [(k, v) for k, v in list_countries.items()],
                key=(lambda name: name[1])
            )
        ),
        initial='',

        widget=forms.Select(
            attrs={
                'class': 'country'
            }
        ),

        error_messages={
            'required': 'Please pick your country.',
            'invalid': 'Your country looks invalid.'
        }
    )

    def clean_first_name(self):
        return _clean_entitle(self, 'first_name')

    def clean_last_name(self):
        return _clean_entitle(self, 'last_name')

    def clean_city(self):
        return _clean_entitle(self, 'city')

    def is_valid(self):
        return _is_valid(self, forms.Form)


# -- Register: Step 3 (about)
class RegisterAboutForm(forms.Form):
    """
    Account > Register About Form
    """
    specialty = forms.CharField(
        required=True,
        max_length=defaults.DEFAULT_MAX,

        widget=forms.TextInput(
            attrs={
                'class': 'specialty',
                'placeholder': 'Your Specialty'
            }
        ),

        error_messages={
            'required': 'Which kind of development do you do at best?',
            'invalid': 'Your specialty looks invalid.'
        }
    )

    company = forms.CharField(
        required=False,
        max_length=defaults.DEFAULT_MAX,

        widget=forms.TextInput(
            attrs={
                'class': 'company',
                'placeholder': 'Your Company or School'
            }
        )
    )

    freelancing = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(
            attrs={
            'id': 'freelancing-cb',
            'class': 'checkbox-classic'
            }
        )
    )

    hiring = forms.BooleanField(
        required=False,
        initial=False,

        widget=forms.CheckboxInput(
            attrs={
                'id': 'hiring-cb',
                'class': 'checkbox-classic'
            }
        )
    )

    def clean_specialty(self):
        return _clean_entitle(self, 'specialty')

    def clean_company(self):
        return _clean_entitle(self, 'company')

    def is_valid(self):
        return _is_valid(self, forms.Form)


# -- Recover: Root
class RecoverRootForm(forms.Form):
    """
    Account > Recover Root Form
    """
    username = forms.CharField(
        required=True,

        widget=forms.TextInput(
            attrs={
                'class': 'forgot-email',
                'placeholder': 'Please, type your Email here.'
            }
        ),

        error_messages={
            'required': 'Please enter your email address.'
        }
    )

    def is_valid(self):
        return _is_valid(self, forms.Form)


# -- Recover: Proceed
class RecoverProceedForm(forms.Form):
    """
    Account > Recover Proceed Form
    """
    password = forms.CharField(
        required=True,
        min_length=defaults.PWD_LENGTH_MIN,
        max_length=defaults.PWD_LENGTH_MAX,

        widget=forms.PasswordInput(
            attrs={
                'class': 'forgot-password',
                'placeholder': 'Your New Password',
                'pattern': defaults.PATTERN_PWD
            }
        )
    )

    password_confirm = forms.CharField(
        required=True,
        min_length=defaults.PWD_LENGTH_MIN,
        max_length=defaults.PWD_LENGTH_MAX,

        widget=forms.PasswordInput(
            attrs={
                'class': 'forgot-password-confirm',
                'placeholder': 'Confirm your New Password',
                'pattern': defaults.PATTERN_PWD
            }
        )
    )

    def clean_password_confirm(self):
        return _clean_password_confirm(self)

    def is_valid(self):
        return _is_valid(self, forms.Form)


# -- Settings: Root
class SettingsRootUserForm(forms.ModelForm):
    """
    Account > Settings Root Form (User)
    """
    first_name = forms.CharField(
        required=True,
        validators=[_validate_strip],
        max_length=defaults.DEFAULT_MAX,

        widget=forms.TextInput(
            attrs={'class': 'input-main'}
        ),

        error_messages={
            'required': "Please enter your first name.",
            'invalid': "Your first name is invalid.",
        },
    )

    last_name = forms.CharField(
        required=True,
        validators=[_validate_strip],
        max_length=defaults.DEFAULT_MAX,

        widget=forms.TextInput(
            attrs={'class': 'input-main'}
        ),

        error_messages={
            'required': "Please enter your last name.",
            'invalid': "Your last name is invalid.",
        },
    )

    email = forms.EmailField(
        required=True,

        widget=forms.EmailInput(
            attrs={'class': 'input-main'}
        ),

        error_messages={
            'required': 'Please enter your email address.',
            'invalid': 'Enter a valid email address.',
        },
    )

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
        ]

        labels = {
            'first_name': "First Name",
            'last_name': "Last Name",
            'email': "Email",
        }

        help_texts = {
            'first_name': "What's your name? Adam, Matt, Sean?",
            'last_name': "D'angelo, Mullenweg, Parker?",
            'email': "Email will not be publicly displayed.",
        }

    def __init__(self, *args, **kwargs):
        self.uid = kwargs.pop('uid') if 'uid' in kwargs else None
        super(SettingsRootUserForm, self).__init__(*args, **kwargs)

    def clean_first_name(self):
        return _clean_entitle(self, 'first_name')

    def clean_last_name(self):
        return _clean_entitle(self, 'last_name')

    def clean_email(self):
        return _clean_email(self)

    def is_valid(self):
        return _is_valid(self, forms.ModelForm)


class SettingsRootProfileForm(forms.ModelForm):
    """
    Account > Settings Root Form (Profile)
    """
    class Meta:
        model = Profile

        fields = [
            'city',
            'country',
            'specialty',
            'company',
            'website',
            'freelancing',
            'hiring',
        ]

        widgets = {
            'city': forms.TextInput(attrs={'class': 'input-main'}),
            'specialty': forms.TextInput(attrs={'class': 'input-main'}),
            'company': forms.TextInput(attrs={'class': 'input-main'}),
            'website': forms.TextInput(attrs={'class': 'input-main'}),
            'freelancing': forms.CheckboxInput(attrs={'class': 'checkbox-classic'}),
            'hiring': forms.CheckboxInput(attrs={'class': 'checkbox-classic'}),
        }

    def clean_city(self):
        return _clean_entitle(self, 'city')

    def clean_specialty(self):
        return _clean_entitle(self, 'specialty')

    def clean_company(self):
        return _clean_entitle(self, 'company')

    def is_valid(self):
        return _is_valid(self, forms.ModelForm)


# -- Settings: Credentials
class SettingsCredentialsForm(forms.Form):
    """
    Account > Settings Credentials Form
    """
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(forms.Form, self).__init__(*args, **kwargs)

        if self.user.has_usable_password():
            self.fields['current_password'] = forms.CharField(
                required=True,
                validators=[self.validate_current_password],

                widget=forms.PasswordInput(
                    attrs={
                        'class': 'current-password input-main',
                        'placeholder': 'Your Current Password',
                        'pattern': defaults.PATTERN_PWD,
                    }
                ),

                error_messages={
                    'required': 'Please enter your current password.',
                    'invalid': 'Your current password is invalid.'
                }
            )

        self.fields['new_password'] = forms.CharField(
            required=True,
            min_length=defaults.PWD_LENGTH_MIN,
            max_length=defaults.PWD_LENGTH_MAX,
            help_text="Minimum %s characters." % defaults.PWD_LENGTH_MIN,

            widget=forms.PasswordInput(
                attrs={
                    'class': 'new-password input-main',
                    'placeholder': 'Your New Password',
                    'pattern': defaults.PATTERN_PWD,
                    'data-equal': 'verify_password',
                    'data-equal-redirect': '1'
                }
            ),

            error_messages={
                'required': 'Please enter your new password.',
                'invalid': 'Password too short (' + str(defaults.PWD_LENGTH_MIN) + ' to ' + str(defaults.PWD_LENGTH_MAX) + ' chars).'
            }
        )

        self.fields['verify_password'] = forms.CharField(
            required=True,
            min_length=defaults.PWD_LENGTH_MIN,
            max_length=defaults.PWD_LENGTH_MAX,

            widget=forms.PasswordInput(
                attrs={
                    'class': 'verify-password input-main',
                    'placeholder': 'Confirm your New Password',
                    'pattern': defaults.PATTERN_PWD,
                    'data-equal': 'new_password'
                }
            ),

            error_messages={
                'required': 'Please confirm your new password (enter it again).',
                'invalid': 'Passwords do not match'
            }
        )

    def validate_current_password(self, password):
        if not self.user.check_password(password):
            raise ValidationError(None, 'invalid')

    def clean_verify_password(self):
        return _clean_password_confirm(self, 'new_password', 'verify_password')

    def is_valid(self):
        return _is_valid(self, forms.Form)
    

# -- Settings: Notification
class SettingsNotificationForm(forms.ModelForm):
    """
    Account > Settings Notification Form
    """
    class Meta:
        model = Settings

        fields = [
            'email_respond',
            'email_follow',
            'email_follow_add',
            'notif_respond',
            'notif_spot',
            'notif_follow',
            'notif_follow_add',
            'notif_waaave',
        ]

        widgets = {
            'email_respond': forms.CheckboxInput(attrs={'class': 'checkbox-classic'}),
            'email_follow': forms.CheckboxInput(attrs={'class': 'checkbox-classic'}),
            'email_follow_add': forms.CheckboxInput(attrs={'class': 'checkbox-classic'}),
            'notif_respond': forms.CheckboxInput(attrs={'class': 'checkbox-classic'}),
            'notif_spot': forms.CheckboxInput(attrs={'class': 'checkbox-classic'}),
            'notif_follow': forms.CheckboxInput(attrs={'class': 'checkbox-classic'}),
            'notif_follow_add': forms.CheckboxInput(attrs={'class': 'checkbox-classic'}),
            'notif_waaave': forms.CheckboxInput(attrs={'class': 'checkbox-classic'}),
        }

    def is_valid(self):
        return _is_valid(self, forms.ModelForm)
