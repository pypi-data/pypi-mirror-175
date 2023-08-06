__all__ = (
    "CordStoreException",
    "ChannelNotFound",
    "NoAttachmentsFound",
    "InvalidChannelType"
)

class CordStoreException(Exception):
    """Base exception class for CordStore"""
    pass

class ChannelNotFound(CordStoreException):
    """Raised when a channel can not be found"""
    pass

class NoAttachmentsFound(CordStoreException):
    """Raised when no attachments are found in a message"""
    pass

class InvalidChannelType(CordStoreException):
    """Raised when a channel is not a specific type of channel"""
    pass