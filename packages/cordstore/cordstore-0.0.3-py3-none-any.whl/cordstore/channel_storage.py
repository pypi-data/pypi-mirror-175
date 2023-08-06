import discord
from discord.ext import commands

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
    "ChannelStorage",
)

class ChannelStorage:
    """Store files in textchannels using a bot"""
    def __init__(
            self, 
            bot: Union[discord.Client, discord.AutoShardedClient, commands.Bot, commands.AutoShardedBot], 
            channel: Union[discord.TextChannel, int],
            session: aiohttp.ClientSession = None
        ) -> None:

        self.session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        self.bot: discord.Client|discord.AutoShardedClient|commands.Bot|commands.AutoShardedBot = bot

        if isinstance(channel, int):
            self.channel: discord.TextChannel = self.bot.get_channel(channel)
            if not self.channel:
                raise ChannelNotFound("Invalid Channel ID")
        else:
            self.channel: discord.TextChannel = channel

    async def upload_file(
            self,
            file: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase, discord.File],
            filename: Optional[str] = None,
            channel: Union[discord.TextChannel, int] = None
        ) -> UploadedFile:
        """
Upload a file - Supports:
- Paths
- Urls
- Bytes
- discord.File
        """

        if channel:
            if isinstance(channel, int):
                try:
                    _channel = await self.bot.fetch_channel(channel)
                    if isinstance(_channel, discord.TextChannel):
                        raise InvalidChannelType("This channel is not a text channel")
                except discord.NotFound:
                    raise ChannelNotFound("Invalid Channel ID")
            else:
                _channel = channel
        else:
            _channel = self.channel

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

        message = await _channel.send(file=file)

        return UploadedFile(message)

    async def close(self):
        await self.session.close()