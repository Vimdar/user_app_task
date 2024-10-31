
from base64 import b64decode
import io
import os
from shutil import rmtree
from uuid import uuid4

from django.core.files.images import ImageFile
from django.conf import settings
from openai import OpenAI
from openai.types.images_response import ImagesResponse

from apps.user_api.constants import (
    AI_PROFILE_IMAGE_MODEL,
    AI_PROFILE_IMAGE_PROMPT,
    AI_PROFILE_IMAGE_SIZE,
    AI_PROFILE_IMAGE_REPSONSE_FORMAT,
)


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def create_default_profile_pic(
    model: str = AI_PROFILE_IMAGE_MODEL,
    prompt: str = AI_PROFILE_IMAGE_PROMPT,
    size: str = AI_PROFILE_IMAGE_SIZE,
    response_format: str = AI_PROFILE_IMAGE_REPSONSE_FORMAT,
) -> ImagesResponse:
    return client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        response_format=response_format,
    )


def create_profile_picture_file(pfp_response: ImagesResponse = None) -> ImageFile:
    pfp_response = pfp_response or create_default_profile_pic()
    return ImageFile(
        io.BytesIO(
            b64decode(pfp_response.data[0].b64_json)
        ),
        name=f'{uuid4().hex[:8]}.png'
    )


def remove_test_uploads_folder(dir_path):
    '''remove test_uploads dir and any posiible leftovers'''
    if os.path.isdir(dir_path):
        try:
            rmtree(dir_path)
        except FileNotFoundError:
            print('Why are we trying to remove a folder that do not exist?')
            raise
