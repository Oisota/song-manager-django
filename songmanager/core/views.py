from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse

from core.models import Song
from core.forms import SongForm, SongDeleteForm, RegistrationForm

def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('songs'))

    return render(request, 'registration/register.html', {
        'form': form,
    })

@login_required
def home(request):
    return redirect(reverse('songs'))

@login_required
def songs(request):
    """Render song table and handle new song requests"""
    template = 'songs/index.html'
    if request.htmx:
        template = 'songs/table.html'

    if request.method == 'POST':
        form = SongForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()

    songs = Song.objects \
        .filter(user=request.user)

    total_duration = sum([song.duration for song in songs])
    count = songs.count()

    form = SongForm()

    return render(request, template, {
        'form': form,
        'songs': songs,
        'total_duration': total_duration,
        'count': count,
    })

@login_required
def song_search(request):
    search_text = request.POST.get('search-text')
    songs = Song.objects \
        .filter(user=request.user, name__icontains=search_text)
    return render(request, 'songs/search-results.html', {
        'songs': songs,
    })

@login_required
def song_edit(request, song_id):
    """Render edit form and handle song updates"""
    song = Song.objects.get(pk=song_id)
    form = SongForm(instance=song)

    if request.method == 'POST':
        form = SongForm(request.POST)
        form.instance.id = song.id
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            resp.headers['HX-Trigger'] = 'song-update'
            return resp
        

    return render(request, 'songs/edit.html', {
        'form': form
    })

@login_required
def song_delete(request, song_id):
    song = Song.objects.get(pk=song_id)
    form = SongDeleteForm(instance=song)

    if request.method == 'DELETE':
        if form.is_valid():
            print('Form Valid')
            Song.objects.get(pk=song_id).delete()
            resp = HttpResponse(status=204)
            resp.headers['HX-Trigger'] = 'song-update'
            return resp
        else:
            return HttpResponse(400)
        
    return render(request, 'songs/delete.html', {
        'form': form,
    })