import asyncio
import logging
import logging.handlers
import os
from typing import List, Optional
import discord
from discord.ext import commands
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime

client = MongoClient(os.environ.get("DATABASE_URL"))
db = client["IEEECS-bot"]


class Chat(BaseModel):
    user: str
    chat: str
    timestamp: datetime


class CustomBot(commands.Bot):
    def __init__(
            self,
            *args,
            testing_guild_id: Optional[int],
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.testing_guild_id = testing_guild_id

    async def setup_hook(self) -> None:
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"Cogs.{filename[:-3]}")

        # In overriding setup hook,
        # we can do things that require a bot prior to starting to process events from the websocket.
        # In this case, we are using this to ensure that once we are connected, we sync for the testing guild.
        # You should not do this for every guild or for global sync, those should only be synced when changes happen.

        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.

    async def on_member_join(self, member: discord.Member):
        channel: discord.TextChannel = self.get_channel(1172930460091940884)
        await channel.send(
            f"Hi {member.mention}! Welcome to IEEE Computer Society MUJ Community server! "
            f"Head over to customize to get roles and get started."
        )

    async def on_message(self, message: discord.Message):
        if message.author != self.user:
            if message.content:
                chat = Chat(user=message.author.name, chat=message.content, timestamp=message.created_at)
                collection = db[f"{message.guild.name}"]
                try:
                    collection.insert_one(chat.model_dump())
                except Exception as e:
                    print(e)


async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    intents = discord.Intents.default()
    intents.message_content = True
    await CustomBot(command_prefix="!", intents=intents, testing_guild_id=1112083866618966076).start(
        os.getenv("DISCORD_TOKEN"))


asyncio.run(main())
