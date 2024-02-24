"""App Forms"""

from django.forms import ModelForm, HiddenInput
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit

from core.models import Song, User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary'))


class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = ['name', 'duration', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-song-form'
        self.helper.attrs['hx-post'] = reverse('songs')
        self.helper.attrs['hx-target'] = '#song-table-view'
        self.helper.attrs['hx-trigger'] = 'click from:#modal-add-btn'
        self.helper.attrs['hx-on:htmx:after-request'] = 'App.addSongSuccess()'

        if self.instance.id: # song being edited
            self.helper.form_id = f'edit-song-form-{self.instance.id}'
            self.helper.attrs['hx-post'] = reverse('song_edit', kwargs={'song_id': self.instance.id})
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
        self.helper.attrs['hx-delete'] = reverse('song_delete', kwargs={'song_id': self.instance.id})
        self.helper.attrs['hx-trigger'] = 'click from:#modal-delete-btn'
        self.helper.attrs['hx-on:htmx:after-request'] = 'App.deleteSongSuccess()'
        self.helper.layout = Layout(
            HTML('<p>Are you sure you want to delete "{{ form.instance.name }}"?</p>')
            )

    def is_valid(self):
        return True