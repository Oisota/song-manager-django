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
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('songs')