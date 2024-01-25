from .models import Comment
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import WatchlistItem
from django.contrib.auth.models import User

TMDB_API_KEY = "1f00b3f0d90a5ef0e263f5d2a04c4ac9"

def search(request):

    query = request.GET.get('q')
    

    results = []
    if query:
        data = requests.get(f"https://api.themoviedb.org/3/search/{request.GET.get('type')}?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query={query}")
        if not data.json().get('results'):
            error_message = "Invalid search"
            return render(request, 'home/results.html', {"error_message": error_message})

    else:
        error_message = "Please enter a search query"
        return render(request, 'home/results.html', {"error_message": error_message})
    
    return render(request, 'home/results.html', {
        "data": data.json(),
        "type": request.GET.get("type")
    })


def index(request):
    return render(request, 'home/index.html')

def view_tv_detail(request, tv_id):
    data = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB_API_KEY}&language=en-US")
    recommendations = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US")
    return render(request, "home/tv_detail.html", {
        "data": data.json(),
        "recommendations": recommendations.json(),
        "type": "tv"
    })

def view_movie_detail(request, movie_id):
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    recommendations = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US")
    return render(request, "home/movie_detail.html", {
        "data": data.json(),
        "recommendations": recommendations.json(),
        "type": "movie"
    })

def view_trendings_results(request):
    type = request.GET.get("media_type")
    time_window = request.GET.get("time_window")

    trendings = requests.get(f"https://api.themoviedb.org/3/trending/{type}/{time_window}?api_key={TMDB_API_KEY}&language=en-US")
    return JsonResponse(trendings.json())


def comment_page(request, movie_id):
    if request.method == "POST":
        user = request.user
        comment = request.POST.get("comment")

        if not request.user.is_authenticated:
            user = User.objects.get(id=1)

        Comment(comment=comment, user=user, movie_id=movie_id).save()

        return redirect('comment_page', movie_id=movie_id)

    else:
        data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
        title = data.json()["title"]

        comments = reversed(Comment.objects.filter(movie_id=movie_id))

        return render(request, "home/comments.html", {
            "title": title,
            "comments": comments,
            "movie_id": movie_id,
        })
    
def comment_page2(request, tv_id):
    if request.method == "POST":
        user = request.user
        comment = request.POST.get("comment")

        if not request.user.is_authenticated:
            user = User.objects.get(id=1)

        Comment(comment=comment, user=user, movie_id=tv_id).save()

        return redirect('comment_page2', tv_id=tv_id)
    else:
        # GET request
        data = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB_API_KEY}&language=en-US")
        title = data.json()["name"]

        comments = reversed(Comment.objects.filter(movie_id=tv_id))

        return render(request, "home/comments.html", {
            "title": title,
            "comments": comments,
            "tv_id": tv_id,
        })   


@login_required
def home(request):
    return render(request, 'home/index.html')      


def add_movie_to_watchlist(request, movie_id=None):
    add_to_watchlist(request, movie_id=movie_id)
    return redirect('home')

def add_tv_to_watchlist(request, tv_id=None):
    add_to_watchlist(request, tv_id=tv_id)
    return redirect('home')

def add_to_watchlist(request, movie_id=None, tv_id=None):
    # Check if the item is already in the watchlist
    existing_item = WatchlistItem.objects.filter(
        user=request.user,
        movie_id=movie_id,
        tv_show_id=tv_id
    ).first()

    if not existing_item:
        # If not, add it to the watchlist
        watchlist_item = WatchlistItem(
            user=request.user,
            movie_id=movie_id,
            tv_show_id=tv_id
        )
        watchlist_item.save()

def watchlist(request):
    watchlist_items = WatchlistItem.objects.filter(user=request.user)
    return render(request, 'home/watchlist.html', {'watchlist_items': watchlist_items})    

def remove_from_watchlist(request, item_id):
    watchlist_item = get_object_or_404(WatchlistItem, id=item_id)

    if watchlist_item.user == request.user:
        watchlist_item.delete()
        return redirect('watchlist')

    return JsonResponse({'error': 'Forbidden'}, status=403)    