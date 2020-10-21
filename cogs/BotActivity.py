import discord
import random
from discord.ext import commands, tasks


class BotActivity(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.games_list = []
        self.create_games_list()

    def create_games_list(self):
        # Initial Text File Reading
        with open("./lists/rgames.txt", "r") as f:
            self.games_list = f.read().splitlines()

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Bot is online")

    @tasks.loop(seconds=120)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(random.choice(self.games_list)))

    @commands.command(aliases=["addg","addgame"],
                      brief="Add a game to Ribbot's Game Activity List!", description="Every 2 minutes, Ribbot will "
                                                                                      "cycle through a list of "
                                                                                      "'games' that you can add to!")
    async def add_game(self, ctx, *, game_name):
        # Adding to List
        self.games_list.append(game_name)

        # Adding to text file
        with open("./lists/rgames.txt", "a+") as f:
            f.write(f"\n{game_name}")

        await ctx.send(f"You've added {game_name} to Ribbot's library!")


def setup(client):
    client.add_cog(BotActivity(client))
