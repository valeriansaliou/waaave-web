import os, shutil, json, requests
from urlparse import urlparse
import facebook, twitter
from datetime import datetime, timedelta
from PIL import Image, ImageOps, ImageDraw

from gravatar.templatetags import gravatar
from django.conf import settings

from _commons.helpers.cache import CacheHelper

from .models import *
from .exceptions import *


class AvatarHelper(object):
    """
    An helper on avatar operations
    """

    @classmethod
    def initialize(_class, user):
        """
        Initialize avatar for given user (first request)
        """
        return _class.update(user, source='gravatar')


    @classmethod
    def update(_class, user, source='gravatar'):
        """
        Update avatar for given user
        """
        image_url = _class.get_url(user, source)

        if image_url:
            image_binding, image_path, image_extension = _class.fetch(image_url, user, source)

            if image_path and image_extension:
                _class.process(image_path, image_extension, user)

            return image_binding
        else:
            raise Exception("No Avatar URL")


    @staticmethod
    def get_url(user, source):
        """
        Get avatar URL
        """
        if source in settings.SOCIAL_AUTH_BACKENDS:
            social_user = user.social_auth.filter(provider=source).first()

            if not social_user:
                raise Exception("Social User Binding Not Found")

        if source == 'facebook':
            try:
                # Get Facebook profile picture URL
                graph = facebook.GraphAPI(social_user.extra_data['access_token'])
                graph_data = graph.get_object(
                    'me/picture',

                    width=settings.AVATAR_SIZE_ORIGINAL,
                    height=settings.AVATAR_SIZE_ORIGINAL,
                    redirect='false',
                )

                image_url = graph_data['data']['url']
            except StandardError as e:
                raise Exception(str(e))

        elif source == 'twitter':
            try:
                # Get Twitter profile picture URL
                api = twitter.Api(
                    consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
                    consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                    access_token_key=social_user.extra_data['access_token']['oauth_token'],
                    access_token_secret=social_user.extra_data['access_token']['oauth_token_secret'],
                )
                api_data = api.GetUser(user_id=social_user.uid).GetProfileImageUrl()

                image_url = api_data.replace('_normal', '')
            except Exception as e:
                raise Exception(str(e))

        elif source == 'google-oauth2':
            # Get Google+ profile picture URL
            api_url = 'https://profiles.google.com/s2/photos/profile/%s' % social_user.extra_data['id']
            request = requests.get(api_url)

            if request.status_code is 200:
                image_url = request.url
            else:
                raise Exception('Google Avatar Not Found')

        elif source == 'gravatar':
            # Get from Gravatar
            image_url = gravatar.gravatar_for_email(user.email, size=settings.AVATAR_SIZE_ORIGINAL, default=False)

        elif source == 'url':
            # Get from URL
            image_url = user.binding.url

        else:
            raise Exception("Unknown Avatar Source")

        return image_url


    @classmethod
    def fetch(_class, image_url, user, source):
        """
        Fetch avatar from provided URL
        """
        # Fetch and store avatar
        avatar_convert = False
        avatar_extension = os.path.splitext(
            urlparse(image_url).path
        )[1][1:] or settings.AVATAR_DEFAULT_EXTENSION

        # Will need to convert avatar format to PNG?
        if not avatar_extension in settings.AVATAR_ALLOWED_EXTENSIONS:
            avatar_convert = True
            avatar_extension = 'png'

        if avatar_extension == 'jpeg':
            avatar_extension = 'jpg'

        avatar_path_bare = './%s/original' % user.id
        avatar_path = os.path.join(
            settings.AVATAR_ROOT,
            '%s.%s' % (avatar_path_bare, avatar_extension),
        )
        avatar_directory = os.path.dirname(avatar_path)

        # Initialize (or re-initialize) the avatar directory
        try:
            shutil.rmtree(avatar_directory)
        except:
            pass

        os.mkdir(avatar_directory)

        # Request avatar
        request = requests.get(image_url, stream=True)

        if request.status_code is 200:
            with open(avatar_path, 'wb') as handle:
                for block in request.iter_content(1024):
                    if not block: break
                    handle.write(block)
        else:
            shutil.copyfile(
                os.path.join(settings.STATIC_SRC_ROOT, settings.AVATAR_DEFAULT_PATH['default']['original']),
                avatar_path
            )

        # Convert the received avatar? (before processing it)
        if avatar_convert:
            _class.convert(avatar_path, to_format='PNG')

        # Normalize the received avatar
        avatar_path, avatar_extension, avatar_mime = _class.normalize(avatar_path_bare, avatar_path, avatar_extension)

        # Write binding
        binding = Binding.objects.get_or_create(user=user)[0]
        binding.mime = avatar_mime
        binding.extension = avatar_extension
        binding.source = source
        binding.save()

        return binding, avatar_path, avatar_extension


    @classmethod
    def convert(_class, image_path, to_format):
        """
        Try to convert unsupported avatar format to given one
        """
        try:
            raw_image = Image.open(image_path)
            converted = Image.new('RGB', raw_image.size, (255,255,255))
            converted.paste(raw_image, raw_image)
            converted.save(image_path)
        except:
            raise AvatarConversionFailure("Avatar Conversion Failed For: %s" % image_path)


    @classmethod
    def normalize(_class, image_path_bare, image_path, image_extension):
        """
        Normalize the original avatar (in a common image format)
        """
        normalized_extension = settings.AVATAR_DEFAULT_EXTENSION
        normalized_mime = settings.AVATAR_DEFAULT_MIME

        normalized_path = os.path.join(
            settings.AVATAR_ROOT,
            '%s.%s' % (image_path_bare, normalized_extension),
        )

        image = Image.open(image_path)
        os.remove(image_path)
        image.save(normalized_path, 'PNG', optimize=True, palette=Image.ADAPTIVE)

        return normalized_path, normalized_extension, normalized_mime
    

    @classmethod
    def process(_class, image_path, image_extension, user):
        """
        Process avatar (generate different avatar sizes)
        """
        sizes = {
            'small': settings.AVATAR_SIZE_SMALL,
            'normal': settings.AVATAR_SIZE_NORMAL,
            'large': settings.AVATAR_SIZE_LARGE,
        }

        for size_human, size_numeric in sizes.items():
            try:
                resized_size = (size_numeric, size_numeric,)
                resized_path_bare = './%s/%s' % (user.id, size_human)
                resized_path = os.path.join(
                    settings.AVATAR_ROOT,
                    '%s.%s' % (resized_path_bare, image_extension),
                )

                image = Image.open(image_path)
                image.thumbnail(resized_size, Image.ANTIALIAS)

                # The PNG encoder should be the only one used at this point...
                if image_extension == 'png':
                    image.save(resized_path, 'PNG', optimize=True, palette=Image.ADAPTIVE)
                elif image_extension == 'jpg':
                    image.save(resized_path, 'JPEG', quality=100, optimize=True, progressive=True)
                else:
                    image.save(resized_path, image_extension.upper())

                # Render the alternative avatar designs
                _class.make_circle(resized_path_bare, image_extension, resized_path, resized_size)
            except IOError as e:
                raise Exception("Could Not Process Avatar > %s" % e)


    @staticmethod
    def make_circle(resized_path_bare, image_extension, resized_path, resized_size):
        """
        Create the circle avatar version
        """
        circle_path = os.path.join(
            settings.AVATAR_ROOT,
            '%s_circle.%s' % (resized_path_bare, image_extension),
        )

        image = Image.open(resized_path)
        mask = Image.new('L', resized_size, 0)

        draw = ImageDraw.Draw(mask) 
        draw.ellipse(
            ((0, 0) + resized_size),
            fill=255,
        )

        output = ImageOps.fit(
            image,
            mask.size,
            centering=(0.5, 0.5)
        )
        output.putalpha(mask)
        output.save(circle_path)


    @staticmethod
    def list_expired(sources=None):
        """
        List expired avatars
        """
        date_threshold = datetime.today() - timedelta(seconds=settings.AVATAR_CACHE_EXPIRITY)
        expired = []

        if sources is not None:
            objects = Binding.objects.filter(source__in=sources)
        else:
            objects = Binding.objects

        return objects.filter(date__lte=date_threshold)
