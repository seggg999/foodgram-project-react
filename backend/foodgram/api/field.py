from django.core.files.base import ContentFile
from rest_framework import serializers
import base64


class Base64ImageField(serializers.ImageField):
    '''Поле загрузки картинки в формате Base64.
    '''
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
