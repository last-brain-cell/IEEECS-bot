import asyncio
import discord
from discord.ext import commands
import os
from openai import OpenAI
from googlesearch import search

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. DO NOT MENTION OPENAI OR CHATGPT AT ALL COSTS. Reply must be "
                   "lower than 1500 characters."
    }
]


def give_response(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    append_message(messages, {"role": "user", "content": prompt})
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    reply = response.choices[0].message.content
    append_message(messages, {"role": "assistant", "content": str(reply)})
    return reply if reply else "I can't keep up with the speed of these questions. One at a time please."


def append_message(repository, message):
    if len(repository) > 5:
        repository.pop(1)
    repository.append(message)


def google_search(query):
    for link in search(query, tld="co.in", num=10, stop=10, pause=2):
        return link


class Commands(commands.Cog, name="commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def do_something(self, ctx: commands.Context):
        await ctx.send(
            embed=discord.Embed(
                title="Hello", color=0xffd500
            )
        )

    @commands.command()
    @commands.cooldown(rate=3, per=3600)
    async def chatgpt(self, ctx: commands.Context):
        await ctx.send("Enter Prompt...")

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            user_response = await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(title="You didn't respond in time.", color=0xffd500))
        else:
            await ctx.send(
                f"'{user_response.author}' entered: '{user_response.content}' in channel: '{user_response.channel}'\n{user_response.author.mention} Generating Response...")
            await ctx.send(
                embed=discord.Embed(title="AI Generated Response", color=0xffd500).add_field(name="Response: ",
                                                                                             value=give_response(
                                                                                                 user_response.content)))

    @chatgpt.error
    async def chatgpt_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed=discord.Embed(title=f"This command is on cooldown. Try again in {error.retry_after:.2f} seconds.",
                                    color=0xffd500))

    @commands.command()
    async def search(self, ctx):
        await ctx.send("What would you like to search?")

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            user_response = await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(title="You didn't respond in time.", color=0xffd500))
        else:
            await ctx.send(
                f"'{user_response.author}' searched: '{user_response.content}' in channel: '{user_response.channel}'\n{user_response.author.mention} Searching...")
            await ctx.send(
                embed=discord.Embed(title="Search Results", description=google_search(user_response.content), color=0xffd500))


async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))
