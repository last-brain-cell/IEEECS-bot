import asyncio
import datetime
import discord
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo
import requests
from pydantic import BaseModel

subreddits = ['python', "Technology", "Coding", "Webdev", "Cybersecurity", "msp", "Artificial"]
limit = 1
timeframe = 'day'  # hour, day, week, month, year, all
listings = ["top", "best", "new", "hot", "rising", "controversial", "random"]
posts = list()

channels = {
    "python": 1172149798321799168,
    "Technology": 1172150087279980666,
    "Coding": 1172150120846999592,
    "Webdev": 1172150157807202326,
    "Cybersecurity": 1172150191009304617,
    "msp": 1172150223913615541,
    "Artificial": 1172150274081685544
}

class Listing(BaseModel):
    subreddit: str = ""
    listing_type: str = ""
    title: str = ""
    text: str = ""
    url: str = ""
    ups: int = ""

    def display_listing(self):
        display = {
            "subreddit": self.subreddit,
            "listing_type": self.listing_type,
            "title": self.title,
            "text": self.text,
            "url": self.url,
            "ups": self.ups
        }
        return display

    def request_successful(self):
        if self.title == self.text == self.url == "" and self.ups == 0:
            return False
        return True


def get_reddit(subreddit, listing, limit, timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers={'User-agent': 'mybot'})

        r = request.json()
        listing = Listing(
            subreddit=subreddit,
            listing_type=listing,
            title=r["data"]["children"][0]["data"]["title"],
            text=r["data"]["children"][0]["data"]["selftext"],
            url=r["data"]["children"][0]["data"]["url"],
            ups=r["data"]["children"][0]["data"]["ups"]
        )
    except:
        listing = Listing(subreddit=subreddit, listing_type=listing)
    return listing


class Reddit(commands.Cog, name="reddit"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.send_reddits.start()
        ...

    @tasks.loop(seconds=1)
    async def send_reddits(self):
        now: datetime.datetime = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
        tomorrow = datetime.datetime(
            now.year, now.month, now.day, 18, 28, 0, 0, ZoneInfo("Asia/Kolkata")
        ) + datetime.timedelta(days=1)
        await asyncio.sleep((tomorrow - now).seconds)
        guild: discord.Guild = self.bot.get_guild(1112083866618966076)  # test Guild for now

        try:
            for subreddit in subreddits:
                flag = 0
                for listing in listings:
                    if flag == 1:
                        break
                    r = get_reddit(subreddit, listing, limit, timeframe)
                    if not r.request_successful():
                        continue
                    else:
                        posts.append(r.display_listing())
                        flag = 1

            for post in posts:
                embed = discord.Embed(color=0xffd500)
                embed.set_image(url="https://www.freeiconspng.com/thumbs/reddit-icon/red-reddit-icon-7.png",)
                embed.add_field(
                    name=f"r/{post['subreddit']}", value=post["listing_type"]
                )
                embed.add_field(
                    name=post["title"], value=" ", inline=False
                )
                embed.add_field(
                    name=" ", value=post["text"], inline=False
                )
                embed.add_field(
                    name="Ups: ", value=post["ups"], inline=True
                )
                embed.set_author(
                    name="Click this to open post",
                    url=post["url"]
                )
                channel: discord.TextChannel = guild.get_channel(channels.get(post["subreddit"]))  # test channel for now
                await channel.send(f"<&1112083866618966076>\nCheck this out...", embeds=[embed])
        except Exception as e:
            print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(Reddit(bot))
