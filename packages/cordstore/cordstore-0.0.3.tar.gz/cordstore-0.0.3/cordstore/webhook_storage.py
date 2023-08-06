import discord
from discord import Webhook

import os
import io
import aiohttp
from urllib.parse import urlparse
from pathlib import Path

from typing import (
    Union,
    Optional,
    Any
)

from .errors import *
from .uploaded_file import UploadedFile

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
            file: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase, discord.File],
            filename: Optional[str] = None,
        ) -> UploadedFile:
        """
Upload a file - Supports:
- Paths
- Urls
- Bytes
- discord.File
        """
        if isinstance(file, discord.File):
            _file = _file
        else:
            if isinstance(file, str):
                if file[:7] == "http://" or file[:8] == "https://":
                    async with self.session.get(file) as resp:
                        if resp.status == 200:
                            _file = discord.File(io.BytesIO(await resp.read()), Path(urlparse(file).path).name)
                else:
                    _file = discord.File(file, filename)
            else:
                _file = discord.File(file, filename)

        message = await self.webhook.send(file=_file, wait=True)

        return UploadedFile(message)
    
    async def close(self):
        await self.session.close()