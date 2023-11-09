import asyncio
import datetime
import json
import os
import discord
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo
import requests


def get_news():
    response = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey={os.getenv('NEWS_API_KEY')}"
    )
    news = json.loads(response.content)

    # Do better Filtering for getting tech news
    filtered_articles = [article for article in news["articles"] if not any(keyword.lower() in article["title"].lower() for keyword in ["amazon", "flipkart", "offers", "offer"])]
    return filtered_articles[:10]


class News(commands.Cog, name="news"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.send_news.start()
        ...

    @tasks.loop(seconds=1)
    async def send_news(self):
        now: datetime.datetime = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
        tomorrow = datetime.datetime(
            now.year, now.month, now.day, 0, 0, 0, 0, ZoneInfo("Asia/Kolkata")
        ) + datetime.timedelta(days=1)
        await asyncio.sleep((tomorrow - now).seconds)
        guild: discord.Guild = self.bot.get_guild(1112083866618966076)  # test Guild for now

        try:
            channel: discord.TextChannel = guild.get_channel(1172224969086877826)  # test channel for now
            await channel.send(f"{guild.default_role.mention}\nHere are the Top News Articles...")
            for news in get_news():
                embed = discord.Embed(color=0xffd500)
                embed.set_image(url="https://www.freeiconspng.com/thumbs/reddit-icon/red-reddit-icon-7.png", )
                embed.add_field(
                    name=news["title"], value="", inline=False
                )
                embed.add_field(
                    name="Description", value=news["description"], inline=False
                )
                if news["content"] is not None:
                    embed.add_field(
                        name="Content", value=news["content"], inline=False
                    )
                embed.add_field(
                    name="Source", value=news["source"]["name"], inline=True
                )
                embed.add_field(
                    name="Author", value=news["author"], inline=True
                )
                embed.set_author(
                    name="Click here to read the full article",
                    url=news["url"]
                )
                await channel.send(embeds=[embed])
        except Exception as e:
            print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(News(bot))
