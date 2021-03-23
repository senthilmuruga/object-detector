from django.core.exceptions import ValidationError


def file_size(value):
    filesize = value.size
    if filesize > 50000000:
        raise ValidationError("maximum size is 50MB")
