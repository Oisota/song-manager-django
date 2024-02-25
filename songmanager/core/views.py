from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET, require_http_methods
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

    form = SongForm()

    if request.method == 'POST':
        form = SongForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()

    if 'search-text' in request.GET:
        if request.htmx:
            template = 'songs/search-results.html'

        search_text = request.GET.get('search-text')
        songs = Song.objects \
            .filter(user=request.user, name__icontains=search_text) \
            .order_by('name')
    else:
        songs = Song.objects \
            .filter(user=request.user) \
            .order_by('name')

    total_duration = sum([song.duration for song in songs])
    count = songs.count()

    return render(request, template, {
        'form': form,
        'songs': songs,
        'total_duration': total_duration,
        'count': count,
    })

@require_http_methods(['GET', 'POST', 'DELETE'])
@login_required
def song(request, song_id):
    """Handle edit/delete of song"""
    song = Song.objects.get(pk=song_id)

    if request.method == 'GET':
        view = request.GET.get('view', 'edit')
        if view == 'edit':
            form = SongForm(instance=song)
            return render(request, 'songs/edit.html', {
                'form': form
            })
        elif view == 'delete':
            form = SongDeleteForm(instance=song)
            return render(request, 'songs/delete.html', {
                'form': form
            })
    elif request.method == 'POST':
        form = SongForm(request.POST)
        form.instance.id = song.id
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            resp.headers['HX-Trigger'] = 'song-update'
            return resp
    elif request.method == 'DELETE':
        form = SongDeleteForm(instance=song)
        if form.is_valid():
            Song.objects.get(pk=song_id).delete()
            resp = HttpResponse(status=204)
            resp.headers['HX-Trigger'] = 'song-update'
            return resp
        else:
            return HttpResponse(400)