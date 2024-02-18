
from django import template

register = template.Library()

@register.filter
def format_song_duration(duration_seconds):
    """Format song duration into minutes:seconds format"""
    m, s = divmod(duration_seconds, 60)
    return f'{m}:{s:02d}'

@register.filter
def format_total_duration(duration_seconds):
    """Format song duration into minutes:seconds format"""
    m, s = divmod(duration_seconds, 60)
    h, m = divmod(m, 60)
    return f'{h} hours {m:02d} minutes {s:02d} seconds'
