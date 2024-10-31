from os import path
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage, default_storage
from django.db import models

from apps.user_api.utils import create_profile_picture_file


TEST_STORAGE = FileSystemStorage(path.join(settings.MEDIA_ROOT, settings.TEST_UPLOADS_DIR))


def profile_pictures_directory_path(instance, filename: str) -> str:
    return f'pfp/{instance.username}/{uuid4().hex[:8]}_{filename}'


def get_storage() -> str:
    return TEST_STORAGE if settings.DEBUG else default_storage


class MetadataMixin(models.Model):
    '''An abstract mixin to take care of DRY metadata'''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(AbstractUser):
    '''
    This represents the user model of the platform.
    Set as Profile as system user model to differntiate vs user objects created.
    Set AUTH_USER_MODEL to our custom one so can extend/upgrade easier later if needed
    '''
    pass


class User(MetadataMixin):
    '''User objects that are created in this API'''
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    profile_pic = models.ImageField(
        upload_to=profile_pictures_directory_path,
        storage=get_storage,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs) -> None:
        if settings.AI_PROFILE_PICTURES_GENERATION_ENABLED:
            self.profile_pic = create_profile_picture_file()
        return super().save(*args, **kwargs)

    def set_random_profile_pic(self):
        self.profile_pic = create_profile_picture_file()
        self.save(update_fields=['profile_pic', 'updated_at'])
