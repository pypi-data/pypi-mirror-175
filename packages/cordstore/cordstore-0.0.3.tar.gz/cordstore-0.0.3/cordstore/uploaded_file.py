import discord

from .errors import *

from typing import (
    Dict,
    Any,
    Union
)

__all__ = (
    "UploadedFile",
)

class UploadedFile:
    """Represents a uploaded file"""
    def __init__(self, message: Union[discord.Message, discord.WebhookMessage]) -> None:
        self.message: discord.Message = message
        self.id: int = self.message.id
        self.channel_id: int = self.message.channel.id
        if self.message.attachments:
            self.file: discord.Attachment = self.message.attachments[0]
            self.filename: str = self.file.filename
            self.size: int = self.file.size
            self.url: str = self.file.url
            self.proxy_url: str = self.file.proxy_url
            self.width: int|None = self.file.width
            self.height: int|None = self.file.height
            self.content_type: str = self.file.content_type
        else:
            raise NoAttachmentsFound("No attachments were found in message: %s" % self.id)
    
    def to_dict(self) -> Dict[str, Any]:
        payload = {
            'id': self.id,
            'channel_id': self.channel_id,
            'filename': self.filename,
            'size': self.size,
            'url': self.url,
            'proxy_url': self.proxy_url,
            'width': self.width,
            'height': self.height,
            'content_type': self.content_type
        }

        return payload