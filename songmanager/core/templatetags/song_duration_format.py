
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
    h_text = 'hours' if h > 1 else 'hour'
    m_text = 'minutes' if m > 1 else 'minute'
    s_text = 'seconds' if s > 1 else 'second'
    return f'{h} {h_text} {m} {m_text} {s} {s_text}'
