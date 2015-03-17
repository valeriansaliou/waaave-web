from django import forms

from _commons.validators import _is_valid

from models import *


class ReportForm(forms.ModelForm):
    """
    Feedback > Report Form
    """
    class Meta:
        model = Report

        radio_select = lambda: forms.RadioSelect(
            attrs={
                'class': 'radio-classic'
            }
        )

        textarea = lambda: forms.Textarea(
            attrs={
                'class': 'textarea-main',
                'placeholder': 'What do you have to tell us?'
            }
        )

        fields = [
            'satisfaction_general',
            'satisfaction_design',
            'satisfaction_usability',
            'satisfaction_speed',
            'satisfaction_mobile',
            'satisfaction_search',
            'feature_relevant',
            'feature_irrelevant',
            'feature_suggested',
            'feature_ideas',
            'custom_message',
        ]

        widgets = {
            'satisfaction_general': radio_select(),
            'satisfaction_design': radio_select(),
            'satisfaction_usability': radio_select(),
            'satisfaction_speed': radio_select(),
            'satisfaction_mobile': radio_select(),
            'satisfaction_search': radio_select(),
            'feature_relevant': radio_select(),
            'feature_irrelevant': radio_select(),
            'feature_suggested': radio_select(),
            'feature_ideas': textarea(),
            'custom_message': textarea(),
        }

    def is_valid(self):
        return _is_valid(self, forms.ModelForm)
