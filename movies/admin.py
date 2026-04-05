from django.contrib import admin
from .models import Movie, Genre

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display  = ['title', 'status', 'quality', 'imdb_score', 'is_featured', 'views']
    list_filter   = ['status', 'genres', 'quality', 'rating']
    search_fields = ['title', 'director', 'cast']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'status']
    fieldsets = (
        ('Basic Info', {'fields': ('title','slug','tagline','description','director','cast','genres')}),
        ('Details',    {'fields': ('release_year','duration','rating','imdb_score','quality','status','is_featured')}),
        ('Media',      {'fields': ('poster','backdrop','og_image_url')}),
        ('Video',      {'fields': ('video_url_hd','video_url_sd','trailer_embed_url')}),
    )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'icon', 'slug']
