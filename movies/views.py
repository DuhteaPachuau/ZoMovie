from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.conf import settings
from .models import Movie, Genre

def _og(title=None, desc=None, image=None):
    return {
        'og_title':       title or settings.SITE_NAME,
        'og_description': desc  or 'Watch free movies online — no signup required.',
        'og_image':       image or settings.OG_DEFAULT_IMAGE,
    }

def home(request):
    return render(request, 'movies/home.html', {
        'featured':    Movie.objects.filter(is_featured=True).first(),
        'now_showing': Movie.objects.filter(status='now_showing')[:8],
        'top_rated':   Movie.objects.filter(status='top_rated').order_by('-imdb_score')[:6],
        'coming_soon': Movie.objects.filter(status='coming_soon')[:6],
        'genres':      Genre.objects.all(),
        **_og('FlickHive — Free Movie Streaming',
              'Stream free movies online in HD. No signup required. Watch now!'),
    })

def movie_list(request):
    movies     = Movie.objects.all()
    q          = request.GET.get('q', '').strip()
    genre_slug = request.GET.get('genre', '')
    status     = request.GET.get('status', '')
    sort       = request.GET.get('sort', '-created_at')

    if q:
        movies = movies.filter(Q(title__icontains=q)|Q(director__icontains=q)|Q(cast__icontains=q))
    if genre_slug:
        movies = movies.filter(genres__slug=genre_slug)
    if status:
        movies = movies.filter(status=status)
    movies = movies.order_by({'imdb':'-imdb_score','year':'-release_year','title':'title'}.get(sort,'-created_at'))

    page = Paginator(movies, 16).get_page(request.GET.get('page'))
    return render(request, 'movies/movie_list.html', {
        'page_obj': page, 'genres': Genre.objects.all(),
        'q': q, 'sel_genre': genre_slug, 'sel_status': status, 'sort': sort,
        **_og(f'All Movies — {settings.SITE_NAME}', 'Browse and stream free movies in HD.'),
    })

def movie_detail(request, slug):
    movie   = get_object_or_404(Movie, slug=slug)
    similar = Movie.objects.filter(genres__in=movie.genres.all()).exclude(id=movie.id).distinct()[:4]
    return render(request, 'movies/movie_detail.html', {
        'movie': movie, 'similar': similar,
        **_og(f'{movie.title} — {settings.SITE_NAME}',
              movie.description[:160],
              movie.get_og_image() or settings.OG_DEFAULT_IMAGE),
    })

def watch(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    Movie.objects.filter(pk=movie.pk).update(views=movie.views + 1)
    return render(request, 'movies/watch.html', {
        'movie': movie,
        'is_trailer': request.GET.get('trailer') == '1',
        **_og(f'Watch {movie.title} — {settings.SITE_NAME}',
              movie.description[:160],
              movie.get_og_image() or settings.OG_DEFAULT_IMAGE),
    })

def genre_view(request, slug):
    genre  = get_object_or_404(Genre, slug=slug)
    movies = Movie.objects.filter(genres=genre)
    page   = Paginator(movies, 16).get_page(request.GET.get('page'))
    return render(request, 'movies/genre_view.html', {
        'genre': genre, 'page_obj': page,
        **_og(f'{genre.name} Movies — {settings.SITE_NAME}',
              f'Watch {genre.name} movies free online on FlickHive.'),
    })

def categories(request):
    return render(request, 'movies/categories.html', {
        'genres': Genre.objects.all(),
        **_og(f'Categories — {settings.SITE_NAME}', 'Browse movies by genre on FlickHive.'),
    })

def about(request):
    total_views = Movie.objects.aggregate(v=Sum('views'))['v'] or 0
    stats = [
        ('🎬', 'Movies', Movie.objects.count()),
        ('🗂', 'Genres', Genre.objects.count()),
        ('👁', 'Total Views', total_views),
    ]
    return render(request, 'movies/about.html', {
        'stats': stats,
        **_og(f'About — {settings.SITE_NAME}', 'Learn about FlickHive — your free movie streaming platform.'),
    })

def contact(request):
    sent = False
    if request.method == 'POST':
        # TODO: hook up Django email backend or a service like Resend/Mailgun
        sent = True
    return render(request, 'movies/contact.html', {
        'sent': sent,
        **_og(f'Contact — {settings.SITE_NAME}', 'Get in touch with the FlickHive team.'),
    })
