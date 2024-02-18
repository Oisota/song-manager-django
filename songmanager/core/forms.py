"""App Forms"""

from django.forms import ModelForm
from django.urls import reverse
from crispy_forms.helper import FormHelper

from core.models import Song

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

        if self.instance.id: # song being edited
            self.helper.form_id = f'edit-song-form-{self.instance.id}'
            self.helper.attrs['hx-post'] = reverse('song_edit', kwargs={'song_id': self.instance.id})