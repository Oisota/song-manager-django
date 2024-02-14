from django.shortcuts import render

from core.models import Song

def home(request):
    """Home Page"""

    songs = Song.objects \
        .filter(user=request.user)

    return render(request, 'home.html', {
        'songs': songs,
    })