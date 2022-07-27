import discord
from discord.ext import commands
from datetime import datetime


class Chat(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.greeting_list = ['hello', 'hi', 'yo', 'whats up', 'greetings']
        self.farewell_list = ['bye', 'goodbye', 'farewell', 'see ya']
        self.time_list = ['what time is it', 'what is the time', 'whats the time']

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.mentioned_in(message):
            content_lower = message.clean_content.lower().replace("'", "")

            # Greeting
            if [x for x in self.greeting_list if (x in content_lower)]:
                await message.channel.send(f"Hello, {message.author.display_name}!")

            # Farewell
            elif [x for x in self.farewell_list if (x in content_lower)]:
                await message.channel.send(f"Goodbye, {message.author.display_name}!")

            # What time is it?
            elif [x for x in self.time_list if (x in content_lower)]:
                timestamp = datetime.now()
                timestamp = timestamp.strftime(r"%I:%M %p")
                await message.channel.send(f"The current time is {timestamp}.")


def setup(client):
    client.add_cog(Chat(client))
