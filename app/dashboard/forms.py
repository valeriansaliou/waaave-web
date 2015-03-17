import bbcode

from django import forms
from django.core.exceptions import ValidationError

from tag.fields import TagField

from _commons.helpers.levels import LevelsHelper
from _commons.validators import _is_valid


# -- Tutorial: New
class TutorialNewForm(forms.Form):
    """
    Dashboard > Tutorial New Form
    """
    def validate_content(value):
        try:
            if bbcode.validate(value):
                raise
        except Exception:
            raise ValidationError('BBCode is invalid. A tag might not be closed properly.', code='invalid')

    # Mandatory
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'tutorialTitle',
                'class': 'tutorial-title',
                'placeholder': 'Type your title here',
        }),

        error_messages={
            'required': 'Please give a title to your tutorial.',
            'invalid': 'The tutorial title does not seem valid.'
        }
    )
    tags = TagField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'tutorialTags',
                'class': 'tutorial-tags',
                'placeholder': 'Type your tags here',
        }),

        error_messages={
            'required': 'Please attach some tags to your tutorial.',
            'invalid': 'Some of your tags seem to be invalid (check one is not too long).'
        }
    )
    online = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'id': 'tutorialOnline',
                'class': 'checkbox-slide tutorial-online',
        })
    )
    level = forms.ChoiceField(
        required=True,
        choices=[('', 'Level.')] + LevelsHelper.as_tuples(),
        initial='',
        widget=forms.Select(
            attrs={
            'id': 'tutorialLevel',
            'class': 'tutorial-level',
        }),

        error_messages={
            'required': 'Please select the skill level of your tutorial.',
            'invalid': 'Mhh, seems we got an invalid level.'
        }
    )
    content = forms.CharField(
        required=True,
        validators=[validate_content],
        widget=forms.Textarea(
            attrs={
            'id': 'tutorialContent',
            'class': 'tutorial-content',
        }),

        error_messages={
            'required': 'Please write some content for your tutorial.',
            'invalid': 'Seems like the tutorial content is invalid.'
        }
    )

    # Optional
    moderation_message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
            'id': 'moderationMessage',
            'class': 'moderation-message',
            'placeholder': 'Moderators, type your message right here.',
        }),

        error_messages={
            'required': 'Moderators, please enter a moderation message for the tutorial author.',
            'invalid': 'Your moderation message seems to be invalid.'
        }
    )

    def is_valid(self):
        return _is_valid(self, forms.Form)


# -- Tutorial: New
class UploaderForm(forms.Form):
    """
    Dashboard > Uploader Form
    """
    upload  = forms.FileField()
