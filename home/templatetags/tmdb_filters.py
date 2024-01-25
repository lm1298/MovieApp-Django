# tmdb_filters.py

from django import template
import requests

register = template.Library()
TMDB_API_KEY = "1f00b3f0d90a5ef0e263f5d2a04c4ac9"

@register.filter
def tmdb_movie_url(movie_id):
    # Make API request and return data
    # Example: You need to replace this with your actual API request
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    return data.json()

@register.filter
def tmdb_tv_url(tv_id):
    # Make API request and return data
    # Example: You need to replace this with your actual API request
    data = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB_API_KEY}&language=en-US")
    return data.json()
