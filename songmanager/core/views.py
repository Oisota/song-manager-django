from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from core.models import Song
from core.forms import SongForm

@login_required
def home(request):
    """Home Page"""

    songs = Song.objects \
        .filter(user=request.user)

    form = SongForm()

    return render(request, 'home.html', {
        'form': form,
        'songs': songs,
    })

@login_required
@require_POST
def new_song(request):
    """Handle new song form post"""
    form = SongForm(request.POST)
    form.instance.user = request.user
    if form.is_valid():
        form.save()

    return redirect(reverse('home'))