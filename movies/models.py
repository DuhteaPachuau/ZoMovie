from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField


class Genre(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, default='🎬', help_text='Emoji icon')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Movie(models.Model):
    RATING_CHOICES  = [('G','G'),('PG','PG'),('PG-13','PG-13'),('R','R'),('NR','NR')]
    STATUS_CHOICES  = [('now_showing','Now Showing'),('coming_soon','Coming Soon'),('top_rated','Top Rated')]
    QUALITY_CHOICES = [('4K','4K Ultra HD'),('1080p','Full HD 1080p'),('720p','HD 720p')]

    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True)
    description  = models.TextField()
    tagline      = models.CharField(max_length=300, blank=True)
    director     = models.CharField(max_length=150)
    cast         = models.TextField(help_text='Comma-separated')
    genres       = models.ManyToManyField(Genre)
    release_year = models.PositiveIntegerField()
    duration     = models.PositiveIntegerField(help_text='Minutes')
    rating       = models.CharField(max_length=10, choices=RATING_CHOICES, default='PG')
    imdb_score   = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    # ← CloudinaryField instead of ImageField — uploads go directly to Cloudinary
    poster   = CloudinaryField('poster',   folder='posters',   blank=True, null=True)
    backdrop = CloudinaryField('backdrop', folder='backdrops', blank=True, null=True)

    og_image_url = models.URLField(
        blank=True,
        help_text='Optional: paste a Cloudinary URL for OG/social preview. Leave blank to auto-use poster.'
    )

    video_url_hd      = models.URLField(blank=True, help_text='Direct MP4 link for 1080p')
    video_url_sd      = models.URLField(blank=True, help_text='Direct MP4 link for 480p')
    trailer_embed_url = models.URLField(blank=True)

    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='now_showing')
    quality     = models.CharField(max_length=10, choices=QUALITY_CHOICES, default='1080p')
    is_featured = models.BooleanField(default=False)
    views       = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.slug})

    @property
    def duration_display(self):
        h, m = divmod(self.duration, 60)
        return f'{h}h {m}m'

    @property
    def cast_list(self):
        return [c.strip() for c in self.cast.split(',') if c.strip()]

    def _cloudinary_url(self, field, transformation=''):
        """Build an absolute Cloudinary URL from a CloudinaryField value."""
        if not field:
            return ''
        import cloudinary
        public_id = str(field)
        base = f'https://res.cloudinary.com/{cloudinary.config().cloud_name}/image/upload'
        if transformation:
            return f'{base}/{transformation}/{public_id}'
        return f'{base}/{public_id}'

    def get_poster_url(self):
        """Full URL for displaying the poster in templates."""
        return self._cloudinary_url(self.poster)

    def get_og_image(self):
        """1200x630 landscape URL for OG/Twitter card meta tags."""
        if self.og_image_url:
            return self.og_image_url
        return self._cloudinary_url(
            self.poster,
            transformation='c_fill,w_1200,h_630,g_auto,f_jpg,q_auto'
        )