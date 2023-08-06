import discord
from discord.ext import commands

import os
import io

from typing import (
    Union,
    Optional,
    Any
)

from .errors import *
from .file import File

__all__ = (
    "ChannelStorage",
)

class ChannelStorage:
    """Store files in textchannels using a bot"""
    def __init__(
            self, 
            bot: Union[discord.Client, discord.AutoShardedClient, commands.Bot, commands.AutoShardedBot], 
            channel: Union[discord.TextChannel, int]
        ) -> None:

        self.bot: discord.Client|discord.AutoShardedClient|commands.Bot|commands.AutoShardedBot = bot

        if isinstance(channel, int):
            self.channel: discord.TextChannel = self.bot.get_channel(channel)
            if not self.channel:
                raise ChannelNotFound("Invalid Channel ID")
        else:
            self.channel: discord.TextChannel = channel

    async def upload_file(
            self,
            fp: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase],
            filename: Optional[str] = None,
            channel: Union[discord.TextChannel, int] = None
        ) -> File:
        """Upload a file"""
        file = discord.File(fp, filename)

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

        message = await _channel.send(file=file)

        return File(message)