import asyncio
import datetime
import discord
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo

questions = {
    "1": {
        "q": "Reverse the array",
        "l": "https://www.geeksforgeeks.org/write-a-program-to-reverse-an-array-or-string/",
    },
    "2": {
        "q": "Find the maximum and minimum element in an array",
        "l": "https://www.geeksforgeeks.org/maximum-and-minimum-in-an-array/",
    },
    "3": {
        "q": "Find the \"Kth\" max and min element of an array ",
        "l": "https://practice.geeksforgeeks.org/problems/kth-smallest-element/0",
    }
}


class Questions(commands.Cog, name="questions"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.send_questions.start()
        ...

    @tasks.loop(seconds=1)
    async def send_questions(self):
        now: datetime.datetime = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
        tomorrow = datetime.datetime(
            now.year, now.month, now.day, 0, 0, 0, 0, ZoneInfo("Asia/Kolkata")
        ) + datetime.timedelta(days=1)
        await asyncio.sleep((tomorrow - now).seconds)
        guild: discord.Guild = self.bot.get_guild(1112083866618966076)  # test Guild for now
        channel: discord.TextChannel = guild.get_channel(1171740893225689120)  # test channel for now
        try:
            # with open("../ques.json", "r") as file:
            idx = list(questions.keys())[0]
            question = questions[idx]["q"]
            link = questions[idx]["l"]
            # questions.pop(idx)

            embed = discord.Embed(color=0xffd500)
            embed.add_field(
                name="Question ", value=question, inline=False
            )
            embed.set_author(
                name="Click here to go to the Question",
                url=link
            )
            await channel.send(f"<@&1171834553661399130>\n❓Here is the Daily Problem❓\nThe Grind Continues..🎯", embeds=[embed])
        except Exception as e:
            print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(Questions(bot))
