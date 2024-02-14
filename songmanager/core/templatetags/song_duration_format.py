
from django import template

register = template.Library()

@register.filter
def format_song_duration(duration_seconds):
    """Format song duration into minutes:seconds format"""
    m, s = divmod(duration_seconds, 60)
    return f'{m}:{s:02d}'
