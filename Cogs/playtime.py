import datetime
import time
import discord
from discord.ext import commands, tasks


class Playtime(commands.Cog, name="playtime"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.start_time = time.time()

    @commands.Cog.listener()
    async def on_ready(self):
        self.update_status.start()
        ...

    @tasks.loop(minutes=1)
    async def update_status(self):
        td = datetime.timedelta(seconds=int(round(time.time() - self.start_time)))
        td_sec = td.seconds
        hour_count, rem = divmod(td_sec, 3600)
        minute_count, second_count = divmod(rem, 60)
        await self.bot.change_presence(
            activity=discord.Game(name=f"since {td.days} days, {hour_count} hours, {minute_count} minutes"))


async def setup(bot: commands.Bot):
    await bot.add_cog(Playtime(bot))
