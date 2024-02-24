"""App Forms"""

from django.forms import ModelForm, HiddenInput, MultiWidget, NumberInput
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, MultiWidgetField, MultiField
from crispy_forms.bootstrap import InlineField

from core.models import Song, User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary'))


class SongDurationWidget(MultiWidget):
    """Split duration into separate minutes/seconds inputs"""
    def __init__(self, attrs=None):
        number_attrs = {'max': 60, 'min': 0}
        widgets = [
            NumberInput(attrs=number_attrs),
            NumberInput(attrs=number_attrs)
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            m, s = divmod(value, 60)
            return [m, s]
        return [0, 0]

    def value_from_datadict(self, data, files, name):
        """Convert to whole number of seconds"""
        minutes_str, seconds_str = super().value_from_datadict(data, files, name)
        minutes = int(minutes_str)
        seconds = int(seconds_str)
        return (minutes * 60) + seconds



class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = ['name', 'duration', 'status']
        widgets = {
            'duration': SongDurationWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-song-form'
        self.helper.attrs['hx-post'] = reverse('songs')
        self.helper.attrs['hx-target'] = '#song-table-view'
        self.helper.attrs['hx-trigger'] = 'click from:#modal-add-btn'
        self.helper.attrs['hx-on:htmx:after-request'] = 'App.addSongSuccess()'

        self.helper.layout = Layout(
            'name',
            MultiWidgetField('duration', attrs={'class': 'mb-1'}),
            'status'
        )

        if self.instance.id: # song being edited
            self.helper.form_id = f'edit-song-form-{self.instance.id}'
            self.helper.attrs['hx-post'] = reverse('song', kwargs={'song_id': self.instance.id})
            self.helper.attrs['hx-trigger'] = 'click from:#modal-edit-btn'
            self.helper.attrs['hx-on:htmx:after-request'] = 'App.editSongSuccess()'

class SongDeleteForm(ModelForm):
    class Meta:
        model = Song
        fields = []
        widgets = {'any_field': HiddenInput(),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'delete-song-form'
        self.helper.attrs['hx-delete'] = reverse('song', kwargs={'song_id': self.instance.id})
        self.helper.attrs['hx-trigger'] = 'click from:#modal-delete-btn'
        self.helper.attrs['hx-on:htmx:after-request'] = 'App.deleteSongSuccess()'
        self.helper.layout = Layout(
            HTML('<p>Are you sure you want to delete "{{ form.instance.name }}"?</p>')
            )

    def is_valid(self):
        return True