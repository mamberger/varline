import datetime
from django.db import models
from tinymce.models import HTMLField


class League(models.Model):
    sport = models.CharField(max_length=150)
    country = models.CharField(max_length=250)
    league = models.CharField(max_length=250)
    title = models.CharField(max_length=255, blank=True, null=True)
    include = models.BooleanField(default=False)
    exclude = models.BooleanField(default=True)

    class Meta:
        ordering = ('sport', 'country', 'league')


class Event(models.Model):
    xbet_id = models.IntegerField()
    SPORTS = (
        ('Футбол', 'Футбол'),
        ('Хоккей', 'Хоккей'),
        ('Биатлон', 'Биатлон'),
        ('Единоборства', 'Единоборства'),
        ('UFC', 'UFC'),
        ('Бокс', 'Бокс'),
        ('Баскетбол', "Баскетбол"),
        ('Формула 1', 'Формула 1'),
        ('Волейбол', 'Волейбол'),
        ('Теннис', 'Теннис')
    )
    sport = models.CharField(max_length=50, choices=SPORTS)
    country = models.CharField(max_length=150)
    league = models.CharField(max_length=150)
    stage = models.CharField(max_length=255, blank=True, null=True)
    home = models.CharField(max_length=250)
    away = models.CharField(max_length=250)
    start = models.DateTimeField()
    home_logo = models.URLField(blank=True, null=True)
    away_logo = models.URLField(blank=True, null=True)
    score_home = models.IntegerField(blank=True, null=True)
    score_away = models.IntegerField(blank=True, null=True)
    score_periods = models.CharField(blank=True, null=True, max_length=255)
    time_seconds = models.IntegerField(default=0)
    STATUS = (
        ('prematch', 'prematch'),
        ('live', 'live'),
        ('complete', 'complete'),
    )
    status = models.CharField(max_length=25, choices=STATUS)
    live_status = models.CharField(max_length=250, blank=True, null=True)
    stats = models.JSONField(blank=True, null=True)
    markets = models.JSONField(blank=True, null=True)
    COLORS = (
        ("Жёлтый", "Жёлтый"),
        ("Красный", "Красный"),
        ("Синий", 'Синий'),
        ('Random', 'Random')
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=20, choices=COLORS, default='Random')
    stream = models.TextField(blank=True, null=True)
    include = models.BooleanField(default=False)
    update = models.IntegerField()

    def save(self, *args, **kwargs):
        self.update = datetime.datetime.now().timestamp()
        super().save(*args, **kwargs)


class News(models.Model):
    img = models.URLField(blank=True, null=True)
    video = models.BooleanField(default=False)
    background = models.URLField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=255)
    content = HTMLField(blank=True, null=True)
    reading_time = models.IntegerField(default=8)
    hidden = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
