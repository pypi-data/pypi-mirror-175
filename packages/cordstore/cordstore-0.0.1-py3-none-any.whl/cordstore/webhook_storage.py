import discord
from discord import Webhook

import os
import io
import aiohttp

from typing import (
    Union,
    Optional,
    Any
)

from .errors import *
from .file import File

__all__ = (
    "WebhookStorage",
)

class WebhookStorage:
    """Store files in textchannels using a webhook"""
    def __init__(
            self, 
            webhook_url: str,
            session: aiohttp.ClientSession = None
        ) -> None:

        self.session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        self.webhook: Webhook = Webhook.from_url(webhook_url, session=self.session)

    async def upload_file(
            self,
            fp: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase],
            filename: Optional[str] = None,
        ) -> File:
        """Upload a file"""
        file = discord.File(fp, filename)

        message = await self.webhook.send(file=file, wait=True)

        return File(message)
    
    async def close(self):
        await self.session.close()