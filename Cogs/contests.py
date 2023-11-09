import asyncio
import datetime
import os
import aiohttp
import discord
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo
import re


class Contests(commands.Cog, name="contests"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.update_contests.start()
        # self.reminder.start()
        ...

    @tasks.loop(seconds=1)
    async def update_contests(self):
        now: datetime.datetime = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
        tomorrow = datetime.datetime(
            now.year, now.month, now.day, 0, 0, 0, 0, ZoneInfo("Asia/Kolkata")
        ) + datetime.timedelta(days=1)
        await asyncio.sleep((tomorrow - now).seconds)
        headers = {"Authorization": os.getenv("CLIST_API_KEY")}
        guild: discord.Guild = self.bot.get_guild(1112083866618966076)
        channel: discord.TextChannel = guild.get_channel(1171740893225689120)
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                     f"https://clist.by:443/api/v3/contest/?upcoming=true&format_time=false&start_time__during="
                    f"1%20day&resource=codingcompetitions.withgoogle.com%2Cleetcode.com%2Ccodechef.com%2"
                    f"Ccodeforces.com&order_by=start",
                    headers=headers,
                ) as response:
                    data = await response.json()
                    if len(data["objects"]) == 0:
                        return
                    embeds = []
                    for obj in data["objects"]:
                        if (
                            discord.utils.get(
                                guild.scheduled_events,
                                location=obj["href"],
                            )
                            is None
                        ) or True:
                            name = re.sub(r"\([^()]*\)", "", obj["event"]).strip()
                            try:
                                event: discord.ScheduledEvent = await guild.create_scheduled_event(
                                    name=f"{name} by {obj['host']}",
                                    description=f"{name} by {obj['host']}\n\n{obj['href']}",
                                    start_time=datetime.datetime.strptime(
                                        obj["start"],
                                        "%Y-%m-%dT%H:%M:%S",
                                    ).replace(tzinfo=datetime.timezone.utc),
                                    end_time=datetime.datetime.strptime(
                                        obj["end"], "%Y-%m-%dT%H:%M:%S"
                                    ).replace(tzinfo=datetime.timezone.utc),
                                    location=obj["href"],
                                )
                                embed = discord.Embed()
                                embed.add_field(
                                    name="Event Name", value=name, inline=False
                                )
                                embed.add_field(
                                    name="Organizer", value=obj["host"], inline=False
                                )
                                embed.add_field(
                                    name="Time",
                                    value=f"<t:{int(event.start_time.timestamp())}:f>",
                                    inline=False,
                                )
                                embed.set_author(
                                    name="Click here to get reminded", url=event.url
                                )
                                embeds.append(embed)
                            except Exception as E:
                                print(E)
                    await channel.send(
                        f"<@&1171834553661399130> Here is a list of competitive programming events"
                        f" being hosted today!",
                        embeds=embeds,
                    )
            except Exception as E:
                print(E)


async def setup(bot: commands.Bot):
    await bot.add_cog(Contests(bot))
