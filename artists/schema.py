import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from artists.models import Artist, Album, Song


class ArtistType(DjangoObjectType):
    class Meta:
        model = Artist


class AlbumType(DjangoObjectType):
    class Meta:
        model = Album


class SongType(DjangoObjectType):
    class Meta:
        model = Song

# Queries


class Query(ObjectType):
    artist = graphene.Field(ArtistType, id=graphene.Int())
    album = graphene.Field(AlbumType, id=graphene.Int())
    song = graphene.Field(SongType, id=graphene.Int())

    def resolve_artist(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Artist.objects.get(id=id)

        return None

    def resolve_album(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Album.objects.get(id=id)

        return None

    def resolve_song(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Song.objects.get(id=id)

        return None

    def resolve_artists(self, info, **kwargs):
        return Artist.objects.all()

    def resolve_albums(self, info, **kwargs):
        return Album.objects.all()

    def resolve_songs(self, info, **kwargs):
        return Song.objects.all()


class ArtistInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    link = graphene.String()
    image = graphene.String()
    genres = graphene.String()


class AlbumInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    release_date = graphene.String()
    link = graphene.String()


class AlbumArtisttInput(graphene.InputObjectType):
    id = graphene.ID()
    album_id = graphene.ID()
    artist_id = graphene.ID()


class SongInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    album_id = graphene.ID()

# Mutations


class CreateArtist(graphene.Mutation):
    class Arguments:
        input = ArtistInput(required=True)

    artist = graphene.Field(ArtistType)

    @staticmethod
    def mutate(root, info, input=None):
        artist_instance = Artist(
            name=input.name,
            link=input.link,
            image=input.image,
            genres=input.genres
        )
        artist_instance.save()
        return CreateArtist(artist=artist_instance)


class UpdateArtist(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ArtistInput(required=True)

    artist = graphene.Field(ArtistType)

    @staticmethod
    def mutate(root, info, input=None):
        artist_instance = Artist.objects.get(pk=id)
        if artist_instance:
            artist_instance.name = input.name
            artist_instance.link = input.link
            artist_instance.image = input.image
            artist_instance.genres = input.genres
            artist_instance.save()
            return UpdateArtist(artist=artist_instance)
        return UpdateArtist(artist=None)


class CreateAlbum(graphene.Mutation):
    class Arguments:
        input = AlbumInput(required=True)

    album = graphene.Field(AlbumType)

    @staticmethod
    def mutate(root, info, input=None):
        artists = []
        for artist_input in input.artists:
            artist = Artist.objects.get(pk=artist_input.id)
            if artist is None:
                return CreateAlbum(album=None)
            artists.append(artist)
        album_instance = Album(
            title=input.title,
            release_date=input.release_date,
            link=input.link
        )
        album_instance.save()
        album_instance.artists.set(artists)
        return CreateAlbum(album=album_instance)


class UpdateAlbum(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = AlbumInput(required=True)

    album = graphene.Field(AlbumType)

    @staticmethod
    def mutate(root, info, id, input=None):
        album_instance = Album.objects.get(pk=id)
        if album_instance:
            artists = []
            for artist_input in input.artists:
                artist = Artist.objects.get(pk=artist_input.id)
                if artist is None:
                    return UpdateAlbum(album=None)
                artists.append(artist)
            album_instance.title = input.title
            album_instance.release_date = input.release_date
            album_instance.link = input.link
            album_instance.save()
            album_instance.artists.set(artists)
            return UpdateAlbum(album=album_instance)
        return UpdateAlbum(album=None)


class CreateSong(graphene.Mutation):
    class Arguments:
        input = SongInput(required=True)

    song = graphene.Field(SongType)

    @staticmethod
    def mutate(root, info, input=None):
        song_instance = Song(
            title=input.title,
            album_id=input.album_id
        )
        song_instance.save()
        return CreateSong(song=song_instance)


class UpdateSong(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = SongInput(required=True)

    song = graphene.Field(SongType)

    @staticmethod
    def mutate(root, info, input=None):
        song_instance = Song.objects.get(pk=id)
        if song_instance:
            song_instance.name = input.name
            song_instance.album_id = input.album_id
            album = Album.objects.get(pk=input.album_id)
            song_instance.save()
            return UpdateSong(song=song_instance)
        return UpdateSong(song=None)


class Mutation(graphene.ObjectType):
    create_artist = CreateArtist.Field()
    update_artist = UpdateArtist.Field()
    create_album = CreateAlbum.Field()
    update_album = UpdateAlbum.Field()
    create_song = CreateSong.Field()
    update_song = UpdateSong.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
