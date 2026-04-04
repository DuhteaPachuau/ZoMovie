import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from movies.models import Genre, Movie

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@flickhive.com', 'admin123')
    print("✓ Admin: admin / admin123")

genres_data = [
    ('Action','action','💥'),('Drama','drama','🎭'),('Comedy','comedy','😂'),
    ('Thriller','thriller','🔪'),('Sci-Fi','sci-fi','🚀'),('Horror','horror','👻'),
    ('Romance','romance','❤️'),('Animation','animation','🎨'),
    ('Fantasy','fantasy','🐉'),('Documentary','documentary','🎥'),
]
for name, slug, icon in genres_data:
    Genre.objects.update_or_create(slug=slug, defaults={'name':name,'icon':icon})
print(f"✓ {Genre.objects.count()} genres")

genres = {g.slug: g for g in Genre.objects.all()}

movies = [
    dict(title='Galactic Horizon',slug='galactic-horizon',
         description="A crew of astronauts embarks on humanity's most daring mission — a one-way voyage beyond the known universe.",
         tagline='Beyond the stars, beyond time.',director='Elena Vasquez',
         cast='Marcus Chen, Sofia Reyes, David Park',release_year=2025,duration=148,
         rating='PG-13',imdb_score=8.7,status='now_showing',quality='4K',is_featured=True,
         video_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',
         trailer_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',
         genres_list=['action','sci-fi']),
    dict(title='The Last Symphony',slug='the-last-symphony',
         description='A legendary composer grappling with hearing loss races to finish his masterwork.',
         tagline="Hear it before it's gone.",director='James Whitmore',
         cast='Helena Voss, Antonio Luca, Grace Kim',release_year=2024,duration=126,
         rating='PG',imdb_score=9.1,status='top_rated',quality='1080p',is_featured=False,
         video_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',trailer_embed_url='',
         genres_list=['drama','romance']),
    dict(title='Neon Wolves',slug='neon-wolves',
         description='In a cyberpunk metropolis, an elite detective hunts an assassin whose kills seem physically impossible.',
         tagline='The city never sleeps. Neither does death.',director='Kai Tanaka',
         cast='Ren Nakamura, Zara Okonkwo, Felix Mercer',release_year=2025,duration=112,
         rating='R',imdb_score=7.9,status='now_showing',quality='1080p',is_featured=False,
         video_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',
         trailer_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',
         genres_list=['thriller','action']),
    dict(title='Laughing in the Rain',slug='laughing-in-the-rain',
         description='Misfit strangers stuck at a monsoon-delayed airport discover the best adventures happen unexpectedly.',
         tagline='Sometimes detours are the destination.',director='Priya Sharma',
         cast='Aiden Walsh, Maya Patel, Carlos Ruiz',release_year=2025,duration=98,
         rating='PG',imdb_score=7.4,status='now_showing',quality='1080p',is_featured=False,
         video_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',trailer_embed_url='',
         genres_list=['comedy','romance']),
    dict(title='Crimson Tide Rising',slug='crimson-tide-rising',
         description='A marine biologist must confront the ancient terror lurking beneath the waves of a haunted coast.',
         tagline='The deep has awakened.',director='Rachel Moore',
         cast='Sam Ellis, Diana Fox, Patrick Yuen',release_year=2025,duration=118,
         rating='R',imdb_score=7.2,status='coming_soon',quality='4K',is_featured=False,
         video_embed_url='',trailer_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',
         genres_list=['horror','thriller']),
    dict(title="Dragon's Cradle",slug='dragons-cradle',
         description='An orphaned farm girl discovers she can communicate with the last living dragons.',
         tagline='Every legend has a beginning.',director='Olga Petrov',
         cast='Lily Chambers, Ethan Frost, Nora Blackwood',release_year=2025,duration=155,
         rating='PG',imdb_score=8.3,status='coming_soon',quality='4K',is_featured=False,
         video_embed_url='',trailer_embed_url='',genres_list=['fantasy','action']),
    dict(title='Pixel Perfect',slug='pixel-perfect',
         description='A beloved studio faces extinction when a tech giant tries to replace all artists with AI.',
         tagline='Art cannot be automated.',director='Tom Briggs',
         cast='Lucy Hart, Joey Kim, Bernard Osei',release_year=2024,duration=104,
         rating='G',imdb_score=8.5,status='top_rated',quality='1080p',is_featured=False,
         video_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',trailer_embed_url='',
         genres_list=['animation','drama']),
    dict(title='Parallel Lives',slug='parallel-lives',
         description='After a freak accident, a physicist can see alternate versions of her life.',
         tagline='Every choice creates a universe.',director='Sarah Jin',
         cast='Nina Lawson, Peter Graf, Amelia Stone',release_year=2025,duration=138,
         rating='PG-13',imdb_score=8.8,status='top_rated',quality='4K',is_featured=False,
         video_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',
         trailer_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',
         genres_list=['sci-fi','drama']),
    dict(title='Midnight Bloom',slug='midnight-bloom',
         description='Two strangers meet every night in their shared dream — until one stops appearing.',
         tagline='Love knows no boundary, not even sleep.',director='Isla Chen',
         cast='Leo Park, Aria Moon, Sam Delacroix',release_year=2025,duration=110,
         rating='PG-13',imdb_score=7.8,status='now_showing',quality='1080p',is_featured=False,
         video_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',trailer_embed_url='',
         genres_list=['romance','fantasy']),
    dict(title='The Forgotten War',slug='the-forgotten-war',
         description='A journalist uncovers footage of a secret military operation erased from history.',
         tagline='Some truths are worth dying for.',director='Michael Torres',
         cast='James Reid, Camille Nguyen, Robert Singh',release_year=2025,duration=141,
         rating='R',imdb_score=7.6,status='coming_soon',quality='1080p',is_featured=False,
         video_embed_url='',trailer_embed_url='https://www.youtube.com/embed/dQw4w9WgXcQ',
         genres_list=['documentary','thriller']),
]

for d in movies:
    g_slugs = d.pop('genres_list')
    movie, created = Movie.objects.get_or_create(slug=d['slug'], defaults=d)
    if created:
        for s in g_slugs:
            if s in genres: movie.genres.add(genres[s])

print(f"✓ {Movie.objects.count()} movies")
print("\n🎬 FlickHive ready!")
print("   Admin: http://127.0.0.1:8000/admin/  →  admin / admin123")
