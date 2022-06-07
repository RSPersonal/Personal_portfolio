""" Amazon S3 storage class

This script returns the location and acl for the specific storage type

"""
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Returns the location and default acl for the static storage
    """
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    """
    Returns the location and default acl for the public media storage
    """
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
