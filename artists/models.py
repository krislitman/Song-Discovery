from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Album(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    artists = models.ManyToManyField(Artist)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Song(models.Model):
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
