import asyncio
import datetime
import discord
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo
from pymongo import MongoClient
import matplotlib.pyplot as plt
from collections import Counter

client = MongoClient("mongodb://localhost:27017/")
db = client["IEEECS-bot"]

stop_words = [
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which",
    "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for",
    "with", "about", "against", "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all",
    "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don",
    "should", "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "couldn", "didn",
    "doesn", "hadn", "hasn", "haven", "isn", "ma", "mightn", "mustn", "needn", "shan", "shouldn",
    "wasn", "weren", "won", "wouldn",
    "ain't", "aren't", "couldn't", "didn't", "doesn't", "don't", "hadn't", "hasn't", "haven't",
    "isn't", "it's", "let's", "ma'am", "mightn't", "mustn't", "shan't", "she's", "shouldn't",
    "that's", "there's", "they're", "wasn't", "we'd", "we'll", "we're", "we've", "weren't",
    "won't", "wouldn't", "you'd", "you'll", "you're", "you've", "!search", "!do_something", "!chatgpt"
]


def dict_to_embed(data: dict, title: str, channel):
    embed = discord.Embed(title=title)
    for key, value in enumerate(data):
        embed.add_field(name=key, value=value)


class Stats(commands.Cog, name="stats"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.send_server_stats.start()
        self.send_user_stats.start()
        ...

    @tasks.loop(seconds=1)
    async def send_server_stats(self):
        now: datetime.datetime = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
        next_week = datetime.datetime(
            now.year, now.month, now.day, 0, 0, 0, 0, ZoneInfo("Asia/Kolkata")
        ) + datetime.timedelta(days=7)
        await asyncio.sleep((next_week - now).seconds)
        guild: discord.Guild = self.bot.get_guild(1171565156619268208)
        channel: discord.TextChannel = guild.get_channel(1172209287297253407)
        try:
            collection = db[guild.name]
            total_words = 0
            total_chars = 0
            time_distribution = Counter()
            word_freq = Counter()

            for document in collection.find():
                message = document["chat"]
                words = message.split()
                total_words += len(words)
                total_chars += len(message)

                # Calculate time distribution
                timestamp = document["timestamp"]
                hour = timestamp.hour
                time_distribution[hour] += 1

                # Count word frequency (excluding stop words)
                for word in words:
                    if word.lower() not in stop_words:
                        word_freq[word] += 1

            # Generate a pie chart for time distribution
            plt.pie(time_distribution.values(), labels=time_distribution.keys(), autopct='%1.1f%%')
            plt.title("Time Distribution of Messages")
            plt.show()

            # Get the most frequently said word (excluding stop words)
            most_frequent_words = [word for word in word_freq if word_freq[word] > 1]
            most_frequent_words.sort(key=lambda word: word_freq[word], reverse=True)

            # Plot the number of words typed in the server by users on a bar graph
            users = collection.distinct("user")
            user_word_counts = Counter()
            for user in users:
                user_messages = collection.find({"user": user})
                user_total_words = sum(len(message["chat"].split()) for message in user_messages)
                user_word_counts[user] = user_total_words

            user_word_counts = dict(user_word_counts)
            plt.bar(user_word_counts.keys(), user_word_counts.values())
            plt.xlabel("Users")
            plt.ylabel("Total Words")
            plt.title("Number of Words Typed by Users")
            plt.xticks(rotation=45)
            plt.show()

            return {
                "TotalWords": total_words,
                "TotalCharacters": total_chars,
                "MostFrequentWords": most_frequent_words,
            }
        except Exception as e:
                print(e)

    @tasks.loop(seconds=1)
    async def send_user_stats(self):
        now: datetime.datetime = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
        next_week = datetime.datetime(
            now.year, now.month, now.day, 0, 0, 0, 0, ZoneInfo("Asia/Kolkata")
        ) + datetime.timedelta(days=7)
        await asyncio.sleep((next_week - now).seconds)
        guild: discord.Guild = self.bot.get_guild(1171565156619268208)
        channel: discord.TextChannel = guild.get_channel(1172209287297253407)
        try:
            collection = db[guild.name]
            user_total_words = 0
            user_total_chars = 0
            user_time_distribution = Counter()
            user_word_freq = Counter()

            for member in guild.members:
                for document in collection.find({"user": member}):
                    message = document["chat"]
                    words = message.split()
                    user_total_words += len(words)
                    user_total_chars += len(message)

                    timestamp = document["timestamp"]
                    hour = timestamp.hour
                    user_time_distribution[hour] += 1

                    for word in words:
                        if word.lower() not in stop_words:
                            user_word_freq[word] += 1

                plt.pie(user_time_distribution.values(), labels=user_time_distribution.keys(), autopct='%1.1f%%')
                plt.title("Time Distribution of Messages by User")
                plt.show()

                user_most_frequent_words = [word for word in user_word_freq if user_word_freq[word] > 1]
                user_most_frequent_words.sort(key=lambda word: user_word_freq[word], reverse=True)

                return {
                    "TotalWords": user_total_words,
                    "TotalCharacters": user_total_chars,
                    "MostFrequentWords": user_most_frequent_words,
                }
        except Exception as e:
            print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))
