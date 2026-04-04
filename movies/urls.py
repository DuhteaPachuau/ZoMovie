from django.urls import path
from . import views

urlpatterns = [
    path('',                   views.home,         name='home'),
    path('movies/',            views.movie_list,   name='movie_list'),
    path('movies/<slug:slug>/',views.movie_detail, name='movie_detail'),
    path('watch/<slug:slug>/', views.watch,        name='watch'),
    path('categories/',        views.categories,   name='categories'),
    path('category/<slug:slug>/', views.genre_view, name='genre_view'),
    path('about/',             views.about,        name='about'),
    path('contact/',           views.contact,      name='contact'),
]
