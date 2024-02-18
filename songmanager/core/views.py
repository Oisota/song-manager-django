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

    total_duration = sum([song.duration for song in songs])
    count = songs.count()

    form = SongForm()

    return render(request, 'home.html', {
        'form': form,
        'songs': songs,
        'total_duration': total_duration,
        'count': count,
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

def song_edit(request, song_id):
    song = Song.objects.get(pk=song_id)
    form = SongForm(instance=song)

    if request.method == 'POST':
        form = SongForm(request.POST)
        form.instance.id = song.id
        form.instance.user = request.user
        if form.is_valid():
            form.save()
        

    return render(request, 'songs/edit.html', {
        'form': form
    })