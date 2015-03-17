from django import forms
from django.core.exceptions import ValidationError

from _commons.validators import _is_valid


class ContactForm(forms.Form):
    """
    Company > Contact Form
    """

    def validate_reason(value):
        if value == 'none' or not value:
            raise ValidationError('', 'required')

    full_name = forms.CharField(
        required=True,

        widget=forms.TextInput(
            attrs={
                'class': 'full_name input-main',
                'placeholder': 'Full Name'
            }
        ),

        error_messages={
            'required': 'What\'s your name?',
            'invalid': 'Invalid name.'
        }
    )

    email = forms.EmailField(
        required=True,

        widget=forms.EmailInput(
            attrs={
                'class': 'email input-main',
                'placeholder': 'E-Mail'
            }
        ),

        error_messages={
            'required': 'What\'s your email address?',
            'invalid': 'Invalid email address.'
        }
    )

    reason = forms.ChoiceField(
        required=True,
        validators=[validate_reason],

        choices=(
            ('none', 'Why do you contact us?'),
            ('support', 'Support request'),
            ('bug', 'Bug report'),
            ('feedback', 'Feedback'),
            ('business', 'Business partnership'),
            ('advertising', 'Advertising'),
            ('legal', 'Legal request'),
            ('other', 'Other (not listed)'),
        ),

        widget=forms.Select(
            attrs={
                'class': 'reason select-main'
            }
        ),

        error_messages={
            'required': 'Why do you contact us?',
            'invalid': 'Invalid reason.'
        }
    )

    message = forms.CharField(
        required=True,

        widget=forms.Textarea(
            attrs={
                'class': 'message textarea-main',
                'placeholder': 'Enter your message. Be brief and precise.'
            }
        ),

        error_messages={
            'required': 'Enter your message.',
            'invalid': 'Invalid message.'
        }
    )

    def is_valid(self):
        return _is_valid(self, forms.Form)
